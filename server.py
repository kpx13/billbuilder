# -*- coding: utf-8 -*-

import os
import tornado.ioloop
from tornado.web import StaticFileHandler
import tornado.web
import tornado.httpserver
from tornado_routes import make_handlers, include

from tornado.options import define
from tornado.options import options as tornado_options_dict
define("environment",   default="dev", help="environment")
define("port",          default=8000, type=int)

# TODO Я полагаю, что это безобразие с 
# сеттингсами и импортами надо отрефакторить.
tornado.options.parse_command_line()
import settings
URL_PREFIX = ''
CURR_PATH = os.path.dirname(os.path.realpath(__file__))

from handlers.basehandler import Home

class Application(tornado.web.Application):
    def __init__(self):
        
        req_handlers = [
            (r'/', Home),
            (r'/static/(.*)', StaticFileHandler, {'path':  CURR_PATH + '/static'}),
            (r'/media/(.*)', StaticFileHandler, {'path': CURR_PATH + '/media'}),
            (r'/ico/(.*)', StaticFileHandler, {'path': CURR_PATH + '/static/images'}),
        ] 
        
        req_handlers.extend(make_handlers(URL_PREFIX,
                (r'/account', include('handlers.account')),
                (r'/user', include('handlers.user')),
                (r'/db', include('handlers.db')),
            ))

        app_env = tornado_options_dict.environment
        app_settings = settings.app_options[ app_env ]
        app_settings.update(settings.default_app_options)

        tornado.web.Application.__init__(self, req_handlers, **app_settings)



def main():
    try:
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(tornado_options_dict.port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()