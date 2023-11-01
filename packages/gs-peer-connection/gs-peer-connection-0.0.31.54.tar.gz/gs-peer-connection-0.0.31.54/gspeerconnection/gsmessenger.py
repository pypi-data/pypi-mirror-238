import logging
import time
import socketio
import ubjson
from multiprocessing.dummy import Pool
import msgpack
import requests

class GSCNodeFunctionReceiverSocket:
    @classmethod
    def create(cls, sio, gsdbs, oncnodefunction, poolsize):
        self = GSCNodeFunctionReceiverSocket()
        self.sio = sio
        self.gsdbs = gsdbs
        self._pool = Pool(self.gsdbs.credentials["poolsize"])
        self.oncnodefunction = oncnodefunction
        self._logger = logging.getLogger(__name__)
        self.poolsize = poolsize

        @self.sio.event
        def connect():
            self._logger.info('oncnodefunction connected')

        def on_success(r):
            pass

        def on_errorPost(error):
            self._logger.exception('cnodefunction failed :' + error)

        @self.sio.event
        def oncnodefunction(id, msg):
            msg1 =  msgpack.unpackb(msg, raw=False)

            self._pool.apply_async(self.oncnodefunction, args=[self.gsdbs, id, msg1],
                                   callback=on_success,
                                   error_callback=on_errorPost)

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}&global=true&poolsize={self.poolsize}')
        self.sio.wait()

    def sendcnodefunctionResult(self, id, msg):
        self.sio.emit("cnodeanswer", id, msg)


class GSCNodeFunctionReceiver:
    def __init__(self, gsdbs, oncnodefunction, poolsize):
        self.sio = socketio.Client()
        self.gsdbs = gsdbs
        self.oncnodefunction = oncnodefunction
        self.poolsize = poolsize

    def startSocket(self):
        GSCNodeFunctionReceiverSocket.create(self.sio, self.gsdbs, self.oncnodefunction, self.poolsize)

    def sendcnodefunctionanswer(self, id, msg):

        encoded = msgpack.packb(msg, use_bin_type=True)

        self.sio.emit("cnodeanswer", {"id": id, "data": encoded})


class GSCNodeFunctionCallerSocket:
    @classmethod
    def create(cls, sio, gsdbs, oncnodefunctionanswer,loadbalancerurl):
        self = GSCNodeFunctionCallerSocket()
        self.sio = sio
        self.gsdbs = gsdbs
        self.loadbalancerurl=loadbalancerurl
        self._logger = logging.getLogger(__name__)
        self.oncnodefunctionanswer = oncnodefunctionanswer

        @self.sio.event
        def connect():
            self._logger.warning('oncnodefunction connected')

        @self.sio.event
        def cnodeanswer(id, message):
            if (type(message) is dict):
                self.oncnodefunctionanswer(self.gsdbs, message)
            else:
                self.oncnodefunctionanswer(self.gsdbs, msgpack.unpackb(message, raw=False))

        connectURL = ""

        if "localhost" in self.loadbalancerurl:
            connectURL = f'{self.loadbalancerurl}'
        else:
            connectURL = self.loadbalancerurl

        self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}&caller=true')
        self.sio.wait()


class GSCNodeFunctionCaller:
    def __init__(self, gsdbs, oncnodefunctionanswer,loadbalancerurl,poolsize):
        self.sio = socketio.Client()
        self.gsdbs = gsdbs
        self.oncnodefunctionanswer = oncnodefunctionanswer
        self._pool = Pool(poolsize)
        self.loadbalancerurl=loadbalancerurl
        self._logger = logging.getLogger(__name__)

    def startSocket(self):
        GSCNodeFunctionCallerSocket.create(self.sio,
                                           self.gsdbs,
                                           self.oncnodefunctionanswer,
                                           self.loadbalancerurl)

    def on_success(self, r):
        self._logger.debug('cnodefunction succeed')

    def on_errorPost(self, error):
        self._logger.exception('cnodefunction failed :' + error)

    def emitFunction(self, sio, target, msg):
        msg["cnodefunction"] = target
        encoded = msgpack.packb(msg, use_bin_type=True)
        sio.emit(target, encoded)

    def sendcnodefunction(self, target, msg):
        time.sleep(self.gsdbs.credentials["cnodesendsleep"])
        self._pool.apply_async(self.emitFunction,
                               args=[self.sio, target, msg],
                               callback=self.on_success,
                               error_callback=self.on_errorPost)
class GSCNodeFunctionCallerRest:
    def __init__(self, gsdbs, oncnodefunctionanswer):

        self.gsdbs = gsdbs
        self.oncnodefunctionanswer = oncnodefunctionanswer
        self._pool = Pool(self.gsdbs.credentials["poolsize"])
        self._logger = logging.getLogger(__name__)

    def on_success(self, r):
        self._logger.debug('cnodefunction succeed')

    def on_errorPost(self, error):
        self._logger.exception('cnodefunction failed :' + str(error))

    def emitFunction(self, target, msg, timeout):
        msg["cnodefunction"] = target

        encoded = ubjson.dumpb(msg)
        try:
            r = requests.post(target, data=encoded, timeout=timeout)
            self.oncnodefunctionanswer(self.gsdbs, ubjson.loadb(r.content))
        except requests.exceptions.Timeout:
            self._logger.exception("timeout")
            self.oncnodefunctionanswer(self.gsdbs, {"error": "true",
                                                    "message": "capacity reached"})
        except requests.exceptions.RequestException as e:
            self._logger.exception("something went very wrong" + str(e))
            self.oncnodefunctionanswer(self.gsdbs, {"error": "true",
                                                    "message": "capacity reached"})

        # sio.emit("oncnodefunction", {"target": target, "data": encoded})

    def sendcnodefunction(self, target, msg, timeout):
        self._pool.apply_async(self.emitFunction,
                               args=[target, msg, timeout],
                               callback=self.on_success,
                               error_callback=self.on_errorPost)
