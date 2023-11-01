import asyncio
from datetime import datetime, timedelta
from fractions import Fraction
from io import BytesIO

import aiohttp
import av


class VideoRecorderFrameBased:
    def __init__(self, gsdbs, target, rate, eventloop):
        self.segment = None
        self.writer = None
        self.gsdbs = gsdbs
        self.target = target
        self.rate = rate
        self.framecounter = 0
        self.filename = None
        self.duration = 0
        self.eventloop = eventloop
        self.is_recording = False

    def start_recording(self, filename):
        self.segment = av.open(BytesIO(), mode='wb', format='mpegts')
        self.writer = self.segment.add_stream('libx264', rate=self.rate)
        self.filename = filename
        self.writer.time_base = Fraction(1, self.rate)
        self.is_recording = True

    def write(self, frame):
        frame.time_base = Fraction(1, self.rate)
        frame.pts = self.framecounter
        self.duration = frame.time
        self.framecounter = self.framecounter + 1
        self.segment.mux(self.writer.encode(frame))

    def stop_recording(self):
        self.is_recording = False
        self.segment.mux(self.writer.encode())
        self.segment.close()
        self.writer = None
        self.framecounter = 0
        segment_data = self.segment.file
        voddate = datetime.utcnow() - timedelta(seconds=self.duration)
        asyncio.run_coroutine_threadsafe(self.saveVodSub(self.duration,
                                                         self.gsdbs,
                                                         segment_data.getbuffer(),
                                                         voddate,
                                                         self.target,
                                                         f"{self.filename}.ts"),
                                         self.eventloop)

    async def saveVodSub(self, duration, gsdbs, gsvoddata, datetime, target, vodFileName):
        storageURL = gsdbs.credentials["baseurl"] + gsdbs.credentials['storageurl'] + f"/vod/{target}"
        data = aiohttp.FormData()
        data.add_field('filePart', gsvoddata, filename=f"{vodFileName}")
        async with aiohttp.ClientSession() as session:
            async with session.post(storageURL, cookies=gsdbs.cookiejar, data=data) as response:
                response.raise_for_status()
        vodstmtn = f"""
                        mutation{{
                        addDTable(
                            dtablename:"gsvod",
                            superDTable:[DTABLE],
                            sriBuildInfo:"${{streamkey}}-${{fragmentid}}",
                            dataLinks:[{{ alias:"streamkey",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"fragmentid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                            {{ alias:"starttime",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:DATETIME}},
                            {{ alias:"segmentlength",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}],
                            data:[["streamkey","fragmentid","starttime","segmentlength"],
                                  ["{target}","{vodFileName}","{datetime}","{duration}"]
                                  ])
                    }}
                    """
        await gsdbs.asyncExecuteStatement(vodstmtn)
