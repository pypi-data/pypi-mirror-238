import ast
import json
import logging
import subprocess
from threading import Thread
from time import sleep
import socketio
from aiortc import RTCPeerConnection, RTCRtpSender, RTCConfiguration, RTCIceServer, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from datetime import datetime

try:
    import picamera
except:
    log = logging.getLogger(__name__)
    log.error("failed to import picamera")

from gspeerconnection.pitrack import PiH264Relay, PiH264CameraOutput

video_trackList = list()
indexmap = {}
pcs = set()
relay = None
microfon = None


class BroadcastThread(Thread):
    def __init__(self, cameraoutput):
        super(BroadcastThread, self).__init__()
        self.cameraoutput = cameraoutput

    def run(self):
        while True:
            buf = self.cameraoutput.nal_queue.get()
            if buf:
                for track in video_trackList:
                    track.write(buf)


class GSPeerConnectionBroadcasterPiCaller:
    def __init__(self, gsdbs, camera, oncommand=None, setChannel=None):
        self.sio = socketio.AsyncClient()
        self.gsdbs = gsdbs
        self.camera = camera
        self._logger = logging.getLogger(__name__)
        self.oncommand = oncommand
        self.setChannel = setChannel

    async def startSocket(self):
        self._logger.debug("start broadcast socket")
        await GSPeerConnectionBroadcasterPiSocketv2.create(self.sio, self.gsdbs, self.camera, self.oncommand,
                                                           self.setChannel)

    def getconnectionurl(self):
        connectURL = self.gsdbs.credentials["signalserver"]

        return f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}'

    async def disconnectClient(self):
        await self.sio.disconnect()


class GSPeerConnectionBroadcasterPiSocket:

    def getPiH264Relay(self, id):
        video_track = PiH264Relay(self.gsdbs.credentials["framerate"])

        video_trackList.append(video_track)
        indexmap[id] = video_trackList.index(video_track)
        return video_track

    def getMicrofonRelay(self):
        global relay, microfon
        if relay is None:
            microfon = MediaPlayer("hw:1", format="alsa", options={
                "channels": "1",
                "sample_rate": "44100"
            })
            relay = MediaRelay()
        return relay.subscribe(microfon.audio)

    @classmethod
    async def create(cls, sio, gsdbs, camera, oncommand, setChannel=None):
        self = GSPeerConnectionBroadcasterPiSocket()

        self.rtconfiList = []
        self._logger = logging.getLogger(__name__)
        self.gsdbs = gsdbs
        self.oncommand = oncommand
        self.setChannel = setChannel
        # picam.append(camera)
        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            for turnserver in self.gsdbs.credentials["turnserver"]:
                self.rtconfiList.append(RTCIceServer(urls=turnserver,
                                                     username=self.gsdbs.credentials["turnuser"],
                                                     credential=self.gsdbs.credentials["turnpw"]
                                                     ))

        camera.resolution = (self.gsdbs.credentials["hres"], self.gsdbs.credentials["vres"])
        camera.framerate = self.gsdbs.credentials["framerate"]
        sleep(1)
        target_bitrate = camera.resolution[0] * \
                         camera.resolution[1] * \
                         camera.framerate * 0.150

        cameraOutput = PiH264CameraOutput()
        broadcast_thread = BroadcastThread(cameraOutput)
        self.sio = sio
        camera.start_recording(
            cameraOutput,
            format="h264",
            profile="constrained",
            bitrate=int(target_bitrate),
            inline_headers=True,
            sei=False,
        )

        broadcast_thread.start()
        self.peerConnections = {}

        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def watcher(id, description):
            self._logger.debug("watcher found")
            if type(description) == str:
                description = ast.literal_eval(description)

            desc = type('new_dict', (object,), description)

            offer = RTCSessionDescription(sdp=description["sdp"], type=description["type"])

            self._logger.debug(str(self.rtconfiList))

            if len(self.rtconfiList) > 0:
                pc = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                pc = RTCPeerConnection()

            self.peerConnections[id] = pc

            video = self.getPiH264Relay(id)
            audio = None

            def channel_log(channel, t, message):
                self._logger.debug("channel(%s) %s %s" % (channel.label, t, message))

            def channel_send(channel, message):
                channel_log(channel, ">", message)
                channel.send(message)

            @pc.on("datachannel")
            def on_datachannel(channel):

                self.setChannel(channel)

                channel_log(channel, "-", "created by remote party")

                def subprocess_cmd(command):
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    proc_stdout = process.communicate()[0].strip()
                    channel_send(channel, json.dumps({"response": proc_stdout.decode()}))

                @channel.on("message")
                def on_message(message):
                    channel_log(channel, "<", message)

                    if isinstance(message, str) and message.startswith("ping"):
                        # reply
                        channel_send(channel, f'{{"ping":"pong","ts":"{datetime.utcnow()} UTC"}}')
                    if isinstance(message, str) and message.startswith('{"type'):
                        # reply
                        self.oncommand(self.gsdbs, json.loads(message))
                    if isinstance(message, str) and message.startswith('{"command'):
                        subprocess_cmd(json.loads(message)["command"])

            transceiver = pc.addTransceiver("video", direction="sendonly")

            capabilities = RTCRtpSender.getCapabilities("video")
            preferences = list(filter(lambda x: x.name == "H264", capabilities.codecs))
            preferences += list(filter(lambda x: x.name == "rtx", capabilities.codecs))
            transceiver.setCodecPreferences(preferences)

            if self.gsdbs.credentials["audio"]:
                pc.addTransceiver("audio", direction="sendonly")
                audio = self.getMicrofonRelay()
                pc.addTrack(audio)

            for t in pc.getTransceivers():
                if t.kind == "video":
                    pc.addTrack(video)

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
        async def joined(id):
            await self.sio.emit("broadcaster", id)

        @self.sio.event
        async def disconnectPeer(id):
            if id in self.peerConnections:
                self._logger.info("Disconnected Peer")
                await self.peerConnections[id].close()
                video_trackList.pop(indexmap[id])
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
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')
        await self.sio.wait()


def channel_log(logger, channel, t, message):
    logger.info("channel(%s) %s %s" % (channel.label, t, message))


def channel_send(logger, channel, message):
    channel_log(logger, channel, ">", message)
    channel.send(message)


class GSPeerConnectionBroadcasterPiSocketv2:

    def getPiH264Relay(self, id):
        video_track = PiH264Relay(self.gsdbs.credentials["framerate"])

        video_trackList.append(video_track)
        indexmap[id] = video_trackList.index(video_track)
        return video_track

    def getMicrofonRelay(self):
        global relay, microfon
        if relay is None:
            microfon = MediaPlayer("hw:1", format="alsa", options={
                "channels": "1",
                "sample_rate": "44100"
            })
            relay = MediaRelay()
        return relay.subscribe(microfon.audio)

    @classmethod
    async def create(cls, sio, gsdbs, camera, oncommand, setChannel=None):
        self = GSPeerConnectionBroadcasterPiSocketv2()

        self.rtconfiList = []
        self._logger = logging.getLogger(__name__)
        self.gsdbs = gsdbs
        self.oncommand = oncommand
        self.setChannel = setChannel
        # picam.append(camera)
        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            for turnserver in self.gsdbs.credentials["turnserver"]:
                self.rtconfiList.append(RTCIceServer(urls=turnserver,
                                                     username=self.gsdbs.credentials["turnuser"],
                                                     credential=self.gsdbs.credentials["turnpw"]
                                                     ))

        camera.resolution = (self.gsdbs.credentials["hres"], self.gsdbs.credentials["vres"])
        camera.framerate = self.gsdbs.credentials["framerate"]
        sleep(1)
        target_bitrate = camera.resolution[0] * \
                         camera.resolution[1] * \
                         camera.framerate * 0.150

        cameraOutput = PiH264CameraOutput()
        broadcast_thread = BroadcastThread(cameraOutput)
        self.sio = sio
        camera.start_recording(
            cameraOutput,
            format="h264",
            profile=self.gsdbs.credentials["h264Profile"],
            inline_headers=self.gsdbs.credentials["inlineHeaders"],
            sei=self.gsdbs.credentials["sei"],
            bitrate=int(target_bitrate),
            # quality=self.gsdbs.credentials["quality"]
        )
        camera.annotate_text = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        broadcast_thread.start()
        self.peerConnections = {}

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

            if len(self.rtconfiList) > 0:
                pc = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                pc = RTCPeerConnection()

            self.peerConnections[id] = pc

            video = self.getPiH264Relay(id)
            audio = None

            transceiver = pc.addTransceiver("video", direction="sendonly")

            capabilities = RTCRtpSender.getCapabilities("video")
            preferences = list(filter(lambda x: x.name == "H264", capabilities.codecs))
            preferences += list(filter(lambda x: x.name == "rtx", capabilities.codecs))
            transceiver.setCodecPreferences(preferences)

            if self.gsdbs.credentials["audio"]:
                pc.addTransceiver("audio", direction="sendonly")
                audio = self.getMicrofonRelay()
                pc.addTrack(audio)

            for t in pc.getTransceivers():
                if t.kind == "video":
                    pc.addTrack(video)

            sendchannel = pc.createDataChannel("sendChannel")

            if setChannel is not None:
                setChannel(sendchannel)
            channel_log(self._logger, sendchannel, "-", "created by local party")

            @sendchannel.on("open")
            def on_open():
                self._logger.info("datachannel open")

            @sendchannel.on("message")
            def on_message(message):

                def subprocess_cmd(command):
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    proc_stdout = process.communicate()[0].strip()
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
                video_trackList.pop(indexmap[id])

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""
        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')

        await self.sio.wait()
