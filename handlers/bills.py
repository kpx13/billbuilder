# -*- coding: utf-8 -*-
from tornado_routes import route

from basehandler import BaseHandler
from models.requisites import RequisitesDB
from forms.db import RequisitesForm
from datetime import datetime

url_base = 'bills'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)
            

@route('create')
class BillCreate(BaseHandler):
    
    def get(self):
        
        items = [{  'name': u'Услуги по поддержке сайта за май 2014г',
                    'unit': u'мес.',      
                    'count': 1,
                    'price': 10000  },
                 {  'name': u'Оплата хостинга',
                    'unit': u'мес.',      
                    'count': 6,
                    'price': 250  },
                 {  'name': u'За красивые глаза',
                    'unit': u'шт.',      
                    'count': 2,
                    'price': 666.6  }]
        
        self.context.update({'title': u'Создание счёта',
                             'module_name': url_base,
                             'sender': RequisitesDB.get_one({'inn': '772160030650'}),
                             'recipient': RequisitesForm(),
                             'bill_num': 128,
                             'items': items,
                             'date': datetime.now(),
                             })
        self.render(tmpl('create'))
    
    """
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        
        if form.validate():
            self.context.update({'title': u'%s | Cоздание' % self._model.get_title(),
                                 'item': self._model.create_from_data(form.data)})
            self.render(tmpl('full'))
        else:
            self.context.update({'title': u'%s | Cоздание | Ошибки' % self._model.get_title(),
                                 'form': form})
            self.render(tmpl('create'))"""