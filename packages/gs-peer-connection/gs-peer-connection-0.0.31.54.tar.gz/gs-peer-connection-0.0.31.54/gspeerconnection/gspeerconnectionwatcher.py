import ast
import asyncio
import threading
import json
import logging
from strenum import StrEnum
import socketio
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCIceServer, RTCConfiguration, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole
from aiortc.mediastreams import MediaStreamError
from aiortc.rtcrtpreceiver import RemoteStreamTrack
from queue import Queue
from gspeerconnection.gsmediarecorder import GSMediaRecorder
from threading import Thread
import time

relay = MediaRelay()


def synchronize_async_helper(to_await):
    async_response = []

    async def run_and_capture_result():
        r = await to_await
        async_response.append(r)

    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    coroutine = run_and_capture_result()
    loop.run_until_complete(coroutine)
    return async_response[0]


class GSCOMMAND(StrEnum):
    PAN = 'pan',
    TILT = 'tilt',
    ZOOM = 'zoom',
    FOCUS = 'focus',
    SNAPSHOT = 'snapshot',
    IRCUT = 'ircut'


class GSPeerConnectionWatcherNew:

    def __init__(self):
        self.sio = None
        self.oncommand = None

    async def sendCommand(self, command: GSCOMMAND, value):
        await self.sio.emit("command", {"type": command, "value": value})

    async def process_frames(self, frame_queue, framerate):
        self.logger.warning(f"starting process frames")
        start_time = time.time()
        frame_count = 0
        fps = framerate
        while True:
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1 / fps:
                current_fps = frame_count / elapsed_time
                # print(f'Async Loop FPS: {elapsed_time:.3f}')
                start_time = time.time()
                frame_count = 0
                frame_data = await frame_queue.get()
                await self.onframe(self.gsdbs, self.target, frame_data, 0)
                frame_queue.task_done()
            await asyncio.sleep(0)

    @classmethod
    async def create(cls, connectionWatcher, gsdbs, target, onframe=None, onmessage=None,
                     on_data_channel=None,
                     ontrack=None, sync=True,
                     framerate=15, ontrackended=None, signalingserver=None):
        self = connectionWatcher
        self.rtconfiList = []
        self.sio = socketio.AsyncClient()
        self.peerConnections = None
        self.gsmediaconsumer = None
        self.gsdbs = gsdbs
        self.onframe = onframe
        self.target = target
        self.onmessage = onmessage
        self.on_data_channel = on_data_channel
        self.ontrack = ontrack
        self.ontrackended = ontrackended
        self.signalingserver = signalingserver
        self.sync = sync
        self.framerate = framerate
        self.logger = logging.getLogger(__name__)

        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["turnserver"],
                                                 self.gsdbs.credentials["turnuser"],
                                                 self.gsdbs.credentials["turnpw"]))

        @self.sio.event
        async def connect():
            self.logger.info('connection established')

        @self.sio.event
        async def bjoined(id, type):
            self.logger.info("broadcaster received")
            await self.sio.emit("broadcaster", {"id": id, "target": self.target, "emitter": "python"})

        @self.sio.event
        async def joined(id):
            self.logger.info("calling broadcaster")
            await self.sio.emit("broadcaster", {"id": id, "target": self.target, "emitter": "watcher"})

        @self.sio.event
        async def broadcaster(id, target, emitter):
            if emitter == "watcher" or emitter == "js":
                return

            if len(self.rtconfiList) > 0:
                self.peerConnections = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                self.peerConnections = RTCPeerConnection()

            self.peerConnections.addTransceiver('video', direction='recvonly')

            @self.peerConnections.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                if self.peerConnections.iceConnectionState == "complete":
                    pass

                if self.peerConnections.iceConnectionState == "failed":
                    await self.peerConnections.close()

            @self.peerConnections.on("track")
            async def on_track(track):
                if track.kind == "video":
                    if self.ontrack is not None:
                        self.logger.info("on track received.Recording started")
                        await self.ontrack(self.gsdbs, track, self.target)
                    if self.onframe is not None:
                        self.logger.info("on track received. onframe started")
                        if self.sync:
                            gsmediaconsumer = GSMediaConsumer(self.gsdbs, self.target, self.onframe, self.framerate)
                        else:
                            gsmediaconsumer = GSMediaConsumerAsync(self.gsdbs, self.target, self.onframe,
                                                                   self.frame_queue)
                        gsmediaconsumer.addTrack(track)
                        await gsmediaconsumer.start()

            @self.peerConnections.on("datachannel")
            def on_datachannel(channel):
                self.on_data_channel(channel)

                @channel.on("message")
                def on_message(message):
                    if isinstance(message, str):
                        self.onmessage(message)

            await self.peerConnections.setLocalDescription(await self.peerConnections.createOffer())
            await self.sio.emit("watcher",
                                {"target": self.target,
                                 "id": id,
                                 "sdp": {"type": self.peerConnections.localDescription.type,
                                         "sdp": self.peerConnections.localDescription.sdp}})

        @self.sio.event
        async def watcher(id, description):
            if self.peerConnections is None:
                if len(self.rtconfiList) > 0:
                    self.peerConnections = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
                else:
                    self.peerConnections = RTCPeerConnection()
                if type(description) == str:
                    description = ast.literal_eval(description)

                offer = RTCSessionDescription(sdp=description["sdp"], type=description["type"])

                self.peerConnections.addTransceiver('video', direction='recvonly')

                @self.peerConnections.on("track")
                async def on_track(track):
                    if track.kind == "video":
                        if self.ontrack is not None:
                            self.logger.info("on track received.Recording started")
                            await self.ontrack(self.gsdbs, track, self.target)
                        if self.onframe is not None:
                            self.logger.info("on track received. onframe started")
                            if self.sync:
                                gsmediaconsumer = GSMediaConsumer(self.gsdbs, self.target, self.onframe, self.framerate)
                            else:
                                gsmediaconsumer = GSMediaConsumerAsync(self.gsdbs, self.target, self.onframe,
                                                                       self.frame_queue)
                            gsmediaconsumer.addTrack(track)
                            await gsmediaconsumer.start()

                @self.peerConnections.on("datachannel")
                def on_datachannel(channel):
                    self.on_data_channel(channel)

                    @channel.on("message")
                    def on_message(message):
                        if isinstance(message, str):
                            self.onmessage(message)

                await self.peerConnections.setRemoteDescription(offer)
                await self.peerConnections.setLocalDescription(await self.peerConnections.createAnswer())
                await self.sio.emit("answer",
                                    {"id": id,
                                     "message": {"type": self.peerConnections.localDescription.type,
                                                 "sdp": self.peerConnections.localDescription.sdp}})

        @self.sio.event
        async def answer(id, description):
            if self.peerConnections.signalingState != "stable":
                if isinstance(description, dict):
                    desc = type('new_dict', (object,), description)
                else:
                    desc = type('new_dict', (object,), ast.literal_eval(description))
                await self.peerConnections.setRemoteDescription(desc)

        @self.sio.event
        async def disconnect():
            self.logger.info("Socket connection list")
            if self.peerConnections != None:
                await self.peerConnections.close()
            if self.gsmediaconsumer != None:
                await self.gsmediaconsumer.stop()
            await self.ontrackended(self.gsdbs, target)

        @self.sio.event
        async def disconnectPeer(id):
            self.logger.info("Camera connection list")
            if self.peerConnections != None:
                await self.peerConnections.close()
            if self.gsmediaconsumer != None:
                await self.gsmediaconsumer.stop()
            await self.ontrackended(self.gsdbs, target)

        if self.signalingserver is not None:
            connectURL = self.signalingserver

        else:
            if "localhost" in self.gsdbs.credentials["signalserver"]:
                connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
            else:
                connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&target={self.target}&terminator=true')

        if self.sync:
            await self.sio.wait()
        else:
            self.frame_queue = asyncio.Queue(3)
            process_task = asyncio.create_task(self.process_frames(self.frame_queue, self.framerate))
            return await asyncio.gather(self.sio.wait(), process_task)


class FrameBufferThread(Thread):
    def __init__(self, gsdbs, target, onframe, framerate):
        super(FrameBufferThread, self).__init__()
        self.gsdbs = gsdbs
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting Buffer")
        self.target = target
        self.onframe = onframe
        self.framerate = framerate
        self.nal_queue = Queue(3)

    def write(self, frame):
        if not self.nal_queue.full():
            self.nal_queue.put(frame)

    def run(self):
        start_time = time.time()
        frame_count = 0
        fps = self.framerate
        while True:
            frame_count += 1
            elapsed_time = time.time() - start_time

            if elapsed_time > 1 / fps:
                try:
                    buf = self.nal_queue.get()
                except Queue.Empty:
                    self.onframe(self.gsdbs, self.target, None, -1)

                if frame_count % 1500 == 0:
                    self.logger.warning("framebufferthread running")
                    frame_count = 0

                start_time = time.time()
                if buf is not None or buf:
                    self.onframe(self.gsdbs, self.target, buf, 15)
                else:
                    self.onframe(self.gsdbs, self.target, None, -1)
            time.sleep(0.01)


class GSMediaConsumer:

    def __init__(self, gsdbs, target, onframe, framerate):
        self.__tracks = {}
        self.gsdbs = gsdbs
        self.target = target
        self.onframe = onframe
        self.nal_queue = Queue(3)
        self.broadcastthread = FrameBufferThread(self.gsdbs, self.target, self.onframe, framerate)
        self.broadcastthread.start()

    def addTrack(self, track):
        if track not in self.__tracks:
            self.__tracks[track] = None

    async def start(self):
        """
        Start discarding media.
        """
        for track, task in self.__tracks.items():
            if task is None:
                self.__tracks[track] = asyncio.ensure_future(
                    self.stream_consume(track, self.gsdbs, self.target, self.onframe))

    async def stream_consume(self, track, gsdbs, target, onframe):
        while True:
            try:
                frame = await track.recv()
                if not self.broadcastthread.is_alive():
                    self.broadcastthread = FrameBufferThread(self.gsdbs, self.target, self.onframe, 15)
                    self.broadcastthread.start()
                self.broadcastthread.write(frame)
            except MediaStreamError:
                pass

    async def stop(self):
        """
        Stop discarding media.
        """
        for task in self.__tracks.values():
            if task is not None:
                task.cancel()
        self.__tracks = {}


class GSMediaConsumerAsync:

    def __init__(self, gsdbs, target, onframe, frame_queue):
        self.__tracks = {}
        self.gsdbs = gsdbs
        self.target = target
        self.onframe = onframe
        self.frame_queue = frame_queue

    def addTrack(self, track):
        if track not in self.__tracks:
            self.__tracks[track] = None

    async def start(self):
        """
        Start discarding media.
        """
        for track, task in self.__tracks.items():
            if task is None:
                self.__tracks[track] = asyncio.ensure_future(
                    self.stream_consume(track, self.gsdbs, self.target, self.onframe))

    async def stream_consume(self, track, gsdbs, target, onframe):
        while True:
            try:
                frame = await track.recv()
                await self.frame_queue.put(frame)
            except MediaStreamError:
                return

    async def stop(self):
        for task in self.__tracks.values():
            if task is not None:
                task.cancel()
        self.__tracks = {}
