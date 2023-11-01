import ast
import json
import logging
import platform
from aiortc import VideoStreamTrack
from av import VideoFrame
# import pyaudio as pyaudio
from datetime import datetime
import socketio
from aiortc import RTCPeerConnection, RTCRtpSender, RTCConfiguration, RTCIceServer, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole

import asyncio
import collections
import time

pcs = set()
relay = None
webcam = None
import numpy as np

_logger = logging.getLogger(__name__)
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=48000,
#                 output=True)

video_tracklist = []


class FPS:
    def __init__(self, avarageof=50):
        self.frametimestamps = collections.deque(maxlen=avarageof)

    def __call__(self):
        self.frametimestamps.append(time.time())
        if len(self.frametimestamps) > 1:
            return len(self.frametimestamps) / (self.frametimestamps[-1] - self.frametimestamps[0])
        else:
            return 0.0


async def checkTerminatorQueue(opqueue,videotrack):
    while True:
        data = await opqueue.get()
        if data is not None:
            await videotrack.write(data, 0)
        await asyncio.sleep(0.001)


async def checkCommandQueue(commandqueue, channellist):
    while True:
        data = await commandqueue.get()
        if data is not None:
            for channel in channellist:
                if channel.readyState == "open":
                    channel.send(data)
                if channel.readyState != "open" and channel.readyState != "connecting":
                    _logger.warning("closing datachannel : " + str(channel.readyState))
                    channellist.remove(channel)
        await asyncio.sleep(0.001)


class TerminatorStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()  # don't forget this!
        self.counter = 0
        height, width = 480, 640
        self.framerate = 0
        self.nal_queue = asyncio.Queue(3)

    async def write(self, frame, framerate=0):
        self.framerate = framerate
        if not self.nal_queue.full():
            await self.nal_queue.put(frame)


    async def recv(self):
        pts, time_base = await self.next_timestamp()

        frame = VideoFrame.from_ndarray(await self.nal_queue.get())
        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        return frame


def create_local_tracks(play_from, decode, device, rtbufsize):
    global relay, webcam

    if play_from:
        player = MediaPlayer(play_from, decode=decode)
        return player.audio, player.video
    else:
        options = {"framerate": "30", "video_size": "640x480", "rtbufsize": rtbufsize}
        if relay is None:
            if platform.system() == "Darwin":
                webcam = MediaPlayer(
                    "default:none", format="avfoundation", options=options
                )
            elif platform.system() == "Windows":
                webcam = MediaPlayer(
                    f"video={device}", format="dshow", options=options
                )
            else:
                webcam = MediaPlayer(f"{device}", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(webcam.video)


def force_codec(pc, sender, forced_codec):
    kind = forced_codec.split("/")[0]
    codecs = RTCRtpSender.getCapabilities(kind).codecs
    transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
    transceiver.setCodecPreferences(
        [codec for codec in codecs if codec.mimeType == forced_codec]
    )


# class MicStreamTrack(MediaStreamTrack):
#     """
#     An audio stream object for the mic audio from the client
#     """
#     kind = "audio"
#
#     def __init__(self, track):
#         super().__init__()
#         self.track = track
#         self._logger = logging.getLogger(__name__)
#
#     async def recv(self):
#         self._logger.error("mic recv()")
#
#         # Get a new PyAV frame
#         frame = await self.track.recv()
#
#         # Convert to float32 numpy array
#         floatArray = frame.to_ndarray(format="float32")
#         samples = np.sin(np.arange(50000) / 20)
#         # stream.write(floatArray.tostring())
#         stream.write(samples.astype(np.float32).tostring())
#
#         # Put these samples into the mic queue
#         # micSampleQueue.put_nowait(floatArray)
#
#         self._logger.error("Put {} samples to mic queue".format(len(floatArray)))


class GSPeerConnectionBroadcasterUniversal:

    @classmethod
    async def create(cls, gsdbs, target, videostream=True, addChannel=None, oncommand=None):
        self = GSPeerConnectionBroadcasterUniversal()
        self.rtconfiList = []
        self.gsdbs = gsdbs
        self.target = target
        self.videostream = videostream
        self.oncommand = oncommand
        self.addChannel = addChannel

        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            self.rtconfiList.append(RTCIceServer(urls=self.gsdbs.credentials["turnserver"],
                                                 username=self.gsdbs.credentials["turnuser"],
                                                 credential=self.gsdbs.credentials["turnpw"]
                                                 ))

        self.sio = socketio.AsyncClient()
        self.peerConnections = {}
        self._logger = logging.getLogger(__name__)
        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def joined(id):
            await self.sio.emit("broadcaster", id)

        @self.sio.event
        async def watcher(id, description):
            if type(description) == str:
                description = ast.literal_eval(description)
            desc = type('new_dict', (object,), description)

            offer = RTCSessionDescription(sdp=description["sdp"], type=description["type"])

            if len(self.rtconfiList) > 0:
                pc = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                pc = RTCPeerConnection()

            pcs.add(pc)

            @pc.on("connectionstatechange")
            async def on_connectionstatechange():
                print("Connection state is %s" % pc.connectionState)
                if pc.connectionState == "failed":
                    await pc.close()
                    pcs.discard(pc)

            @pc.on("track")
            async def on_track(track):
                if track.kind == "video":
                    mediablackhole = MediaBlackhole()
                    mediablackhole.addTrack(track)

            if self.addChannel is not None:
                sendchannel = pc.createDataChannel("terminatorview")
                self.addChannel(sendchannel)

            if videostream:
                audio, video = create_local_tracks(False,
                                                   decode=not True,
                                                   device=self.gsdbs.credentials["webcam"],
                                                   rtbufsize=self.gsdbs.credentials["rtbufsize"])
                if video:
                    video_sender = pc.addTrack(video)
                    force_codec(pc, video_sender, "video/H264")

            await pc.setRemoteDescription(offer)

            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

            await self.sio.emit("answer", {"id": id,
                                           "message": json.dumps(
                                               {"type": pc.localDescription.type,
                                                "sdp": pc.localDescription.sdp})})

        @self.sio.event
        async def command(commandcall):
            self.oncommand(self.gsdbs, commandcall)

        @self.sio.event
        async def disconnectPeer(id):
            if id in self.peerConnections:
                await self.peerConnections[id].close()
                self.peerConnections.pop(id, None)

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.target}')
        await self.sio.wait()


def channel_log(logger, channel, t, message):
    logger.info("channel(%s) %s %s" % (channel.label, t, message))


def channel_send(logger, channel, message):
    channel_log(logger, channel, ">", message)
    channel.send(message)


class GSPeerConnectionBroadcasterUniversalNew:

    @classmethod
    async def create(cls,
                     gsdbs,
                     target,
                     videostream=True,
                     addChannel=None,
                     oncommand=None,
                     videotrack=None,
                     signalingserver=None
                     ):
        self = GSPeerConnectionBroadcasterUniversalNew()
        self.addChannel = addChannel
        self.rtconfiList = []
        self.target = target
        self.gsdbs = gsdbs
        self.videostream = videostream
        self.oncommand = oncommand
        self.videotrack = videotrack
        self.signalingserver = signalingserver

        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            self.rtconfiList.append(RTCIceServer(urls=self.gsdbs.credentials["turnserver"],
                                                 username=self.gsdbs.credentials["turnuser"],
                                                 credential=self.gsdbs.credentials["turnpw"]
                                                 ))

        self.sio = socketio.AsyncClient()
        self.peerConnections = {}
        self._logger = logging.getLogger(__name__)
        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def wjoined(id):
            await self.sio.emit("joined", self.sio.sid)

        @self.sio.event
        async def broadcaster(id, description, emitter):

            if emitter == "watcher":
                return
            if len(self.rtconfiList) > 0:
                pc = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                pc = RTCPeerConnection()
            self.peerConnections[id] = pc

            @pc.on("track")
            async def on_track(track):
                if track.kind == "video":
                    mediablackhole = MediaBlackhole()
                    mediablackhole.addTrack(track)
                # if track.kind == "audio":
                #     micTrack = MicStreamTrack(track)
                #     blackHole = MediaBlackhole()
                #     blackHole.addTrack(micTrack)
                #     await blackHole.start()

            async def on_iceconnectionstatechange():
                print("ICE connection state is ", self.peerConnections[id].iceConnectionState)
                if self.peerConnections[id].iceConnectionState == "failed":
                    await self.peerConnections[id].close()
                if self.peerConnections[id].iceConnectionState == "completed":
                    print("completed")

            self.peerConnections[id]._add_event_handler("iceconnectionstatechange", on_iceconnectionstatechange,
                                                        on_iceconnectionstatechange)

            @pc.on("signalingstatechange")
            async def signalingchange():
                print("change" + pc.signalingState)

            if self.videostream:
                audio, video = create_local_tracks(False,
                                                   decode=not True,
                                                   device=self.gsdbs.credentials["webcam"],
                                                   rtbufsize=self.gsdbs.credentials["rtbufsize"])
                if video:
                    video_sender = pc.addTrack(video)
                    force_codec(pc, video_sender, "video/H264")
            if self.videotrack:
                # terminatorviewtrack = TerminatorStreamTrack()
                # video_tracklist.append(terminatorviewtrack)
                relay = MediaRelay()
                pc.addTrack(relay.subscribe(self.videotrack))

            if self.addChannel is not None:
                sendchannel = pc.createDataChannel("terminatorview")
                self.addChannel(sendchannel)
                channel_log(self._logger, sendchannel, "-", "created by local party")

                @sendchannel.on("open")
                def on_open():
                    self._logger.info("datachannel open")

                @sendchannel.on("message")
                def on_message(message):
                    def subprocess_cmd(command):
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                        proc_stdout = process.communicate()[0].strip()
                        # for line in proc_stdout.decode().split('\n'):
                        channel_send(self._logger, sendchannel, json.dumps({"response": proc_stdout.decode()}))

                    channel_log(self._logger, sendchannel, "<", message)
                    if isinstance(message, str) and message.startswith("ping"):
                        channel_send(self._logger, sendchannel, f'{{"ping":"pong","ts":"{datetime.utcnow()} UTC"}}')
                    if isinstance(message, str) and message.startswith('{"type'):
                        self.oncommand(self.gsdbs, json.loads(message))
                    if isinstance(message, str) and message.startswith('{"command'):
                        subprocess_cmd(json.loads(message)["command"])

            await pc.setLocalDescription(await pc.createOffer())
            await self.sio.emit("watcher", {"target": description,
                                            "id": id,
                                            "sdp": json.dumps(
                                                {"type": pc.localDescription.type,
                                                 "sdp": pc.localDescription.sdp})})

        @self.sio.event
        async def answer(id, description):
            if id in self.peerConnections:
                if self.peerConnections[id].signalingState != "stable":
                    if type(description) == str:
                        description = ast.literal_eval(description)
                    desc = type('new_dict', (object,), description)
                    answer = RTCSessionDescription(sdp=description["sdp"], type=description["type"])
                    await self.peerConnections[id].setRemoteDescription(answer)

        @self.sio.event
        async def disconnectBroadcaster(id, desc):
            if id in self.peerConnections:
                self._logger.info("Disconnected Peer")
                await self.peerConnections[id].close()
                self.peerConnections.pop(id, None)

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""

        if self.signalingserver is not None:
            connectURL = self.signalingserver

        else:
            if "localhost" in self.gsdbs.credentials["signalserver"]:
                connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
            else:
                connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}&target={self.target}&terminator=true')
        await self.sio.wait()


async def createTerminatorView(gsdbs, aioqueue: asyncio.Queue,
                               commandqueue: asyncio.Queue,
                               target,
                               signalingserver=None, oncommand=None):
    datachannelist = []

    def addDatachannel(channel):
        datachannelist.append(channel)

    terminatorviewtrack = TerminatorStreamTrack()

    terminatorviewtask = await asyncio.gather(
        checkCommandQueue(commandqueue, datachannelist),
        checkTerminatorQueue(aioqueue,terminatorviewtrack),
        GSPeerConnectionBroadcasterUniversalNew.create(gsdbs=gsdbs,
                                                       target=target + "terminatorview",
                                                       videostream=False,
                                                       videotrack=terminatorviewtrack,
                                                       signalingserver=signalingserver,
                                                       addChannel=addDatachannel,
                                                       oncommand=oncommand
                                                       ))
    return terminatorviewtask
