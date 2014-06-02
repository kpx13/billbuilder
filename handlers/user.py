# -*- coding: utf-8 -*-
from tornado import web
from tornado_routes import route

from basehandler import BaseHandler, authorized

url_base = 'user'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)


@route('profile', name='profile')
class Profile(BaseHandler):
    
    @authorized
    def get(self):
        self.context.update({'title': u'Профиль',
                             'user': self.user_obj.get_profile()
                        })
        self.render(tmpl('profile'))