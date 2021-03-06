#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer


class MyHanlder(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):

        print self.requestline
        if self.requestline.startswith('GET /_laststats.csv'):
            import requests
            res = requests.get('http://127.0.0.1:8082/S/current')
            print "Overwriting %d" % len(res.text)
            with file('_laststats.csv', 'w+') as fp:
                fp.write(res.text)
            self.wfile.write(res.text)

        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()



if __name__ == '__main__':
    HandlerClass = SimpleHTTPServer.SimpleHTTPRequestHandler
    MyServerClass = BaseHTTPServer.HTTPServer
    BaseHTTPServer.test(MyHanlder, MyServerClass)

   



