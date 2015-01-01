import json
import time
import os.path
import tornado.ioloop
import tornado.web
import tornado.gen

from .bittivahti import Bittivahti

INTERFACE = 'eth0'
MAX_BANDWIDTH = 100*1e6/8 # 10 Mbit/s


BASEDIR = os.path.dirname(__file__)
STATICDIR = os.path.join(BASEDIR, 'static')

class DataHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.set_header('Content-Type', 'text/event-stream; charset="utf-8"')
        self.set_header('Cache-Control', 'no-cache')
        self.bitti = Bittivahti()
        self.iface = INTERFACE
        self._loop()

    def _loop(self):
        bitti = self.bitti
        bitti.update_state()
        rx, tx, rxp, txp = [x/bitti.period for x in bitti.delta[self.iface]]
        rx_t, tx_t, rxp_t, txp_t = bitti.total[self.iface]

        data = dict(rx=rx, tx=tx, rxp=rxp, txp=txp,
                    rx_t=rx_t, tx_t=tx_t, rxp_t=rxp_t, txp_t=txp_t,
                    max=MAX_BANDWIDTH)
        self.write("data: ")
        self.write(json.dumps(data))
        self.write("\n\n")
        self.flush()
        tornado.ioloop.IOLoop.instance().call_later(0.2, self._loop)


application = tornado.web.Application([
    (r'/', tornado.web.RedirectHandler,
        dict(url="/index.html")),
    (r'/(moped\.svg|index\.html)', tornado.web.StaticFileHandler,
        {'path': STATICDIR}),
    (r"/data\.stream", DataHandler),
])


def main():
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
