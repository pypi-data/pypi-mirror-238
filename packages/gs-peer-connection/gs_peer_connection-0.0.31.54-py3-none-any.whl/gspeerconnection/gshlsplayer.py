import logging
import time
from timeit import default_timer as timer
import cv2
import asyncio
import sys

from gspeerconnection.gspeerconnectionwatcher import FrameBufferThread


class GSHLSPlayer:

    def __init__(self, gsdbs, onframe, ondestruct, url):
        self.gsdbs = gsdbs
        self.target = "hls_playlist"
        self.onframe = onframe
        self.ondestruct = ondestruct
        self.url = url
        self.url += f"&vision=true&session={self.gsdbs.cookiejar.get('session')}&signature={self.gsdbs.cookiejar.get('signature')}"
        self._logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(__name__)
        self.broadcastthread = FrameBufferThread(self.gsdbs, self.target, self.onframe)
        self.broadcastthread.start()

    async def startrecording(self):
        cap = cv2.VideoCapture(self.url)
        if cap.isOpened() == False:
            self._logger.error("unable to open playlist")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)
        # fps = 1000
        wait_ms = (1000 / fps)
        self._logger.info(f"playing back HLS-Playlist with {fps} fps")
        framecount = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()

            self.broadcastthread.write(frame)

            end_time = time.time()

            execution_time_ms = (end_time - start_time) * 1000

            calculatedwait = wait_ms - execution_time_ms / 1000
            # self.logger.info(f"frame written with id {framecount}")
            framecount = framecount + 1
            if calculatedwait > 0:
                time.sleep(calculatedwait / 1000)

        self.ondestruct(self.gsdbs)

        cap.release()


class GSHLSPlayerNew:

    def __init__(self, gsdbs, onframe, ondestruct, url, queue):
        self.gsdbs = gsdbs
        self.target = "hls_playlist"
        self.onframe = onframe
        self.ondestruct = ondestruct
        self.url = url
        self.url += f"&vision=true&session={self.gsdbs.cookiejar.get('session')}&signature={self.gsdbs.cookiejar.get('signature')}"
        self._logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(__name__)
        self.queue = queue
        # self.broadcastthread = FrameBufferThread(self.gsdbs, self.target, self.onframe)
        # self.broadcastthread.start()

    async def startrecording(self):
        cap = cv2.VideoCapture(self.url)
        if cap.isOpened() == False:
            self._logger.error("unable to open playlist")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)
        # fps = 1000
        wait_ms = (1000 / fps)
        self._logger.info(f"playing back HLS-Playlist with {fps} fps")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()

            await self.queue.put(frame)

            end_time = time.time()
            execution_time_ms = (end_time - start_time) * 1000
            calculatedwait = wait_ms - execution_time_ms / 1000

            if calculatedwait > 0:
                await asyncio.sleep(calculatedwait / 1000)

        self.ondestruct(self.gsdbs)

        cap.release()


async def checkHLSQueue(opqueue, gsdbs, source, onframe):
    while True:
        data = await opqueue.get()
        if data is not None:
            await onframe(gsdbs, source, data, 0)


async def createHLSPlayer(gsdbs, onframe, source, ondestruct, playlisturl):
    hlsqueue = asyncio.Queue(3)
    hlsplayer = GSHLSPlayerNew(gsdbs, onframe=onframe, ondestruct=ondestruct, url=playlisturl, queue=hlsqueue)
    hlstask = await asyncio.gather(hlsplayer.startrecording(),
                                   checkHLSQueue(hlsqueue, gsdbs, source, onframe))
    return hlstask
