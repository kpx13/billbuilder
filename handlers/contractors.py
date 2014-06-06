# -*- coding: utf-8 -*-
from tornado_routes import route

from basehandler import BaseHandler, authorized
from models.contactor import ContactorDB

url_base = 'contractors'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)

@route('/middle/(.*)')
class ContractorsMiddle(BaseHandler):
    _model = ContactorDB   
    _template_name = tmpl('middle')

    def get(self, _id):
        self.context.update({'title': u'%s | Представление middle' % self._model.get_title(),
                             'item': self._model.get_middle(_id),
                             'module_name': self._name})
        self.render(self._template_name)

@route('')
class ContractorsList(BaseHandler):
    _model = ContactorDB
    
    @authorized
    def get(self):
        self.context.update({'title': u'Контрагенты',
                             'module_name': url_base,
                             'items': self._model.get_table_by_user(self.user_id),
                             'count': self._model.get_count(),
                             'table_cols': self._model.get_table_columns(),
                             })
        self.render(tmpl('list'))