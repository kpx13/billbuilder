# -*- coding: utf-8 -*-
from tornado_routes import route

from basehandler import BaseHandler
from models.requisites import RequisitesDB
from models.contactor import ContactorDB
from models.bill import BillDB
from models.content import ContentDB
from models.user import UserDB
from models.counter import Counter
from forms.db import RequisitesForm, BillContentForm
from datetime import datetime
import logging

url_base = 'bills'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)
            

@route('create')
class BillCreate(BaseHandler):
    
    def get(self):
        
        self.context.update({'title': u'Создание счёта',
                             'module_name': url_base,
                             'sender': RequisitesDB.get_one({'inn': '772160030650'}),
                             'recipient': RequisitesForm(),
                             'bill_content': BillContentForm(),
                             'bill_num': Counter.next_key('bill'),
                             'date': datetime.now(),
                             })
        self.render(tmpl('create'))
    
    
    def post(self, *args, **kwargs):
        recipient_form = RequisitesForm(self.request.arguments)
        bill_content_form = BillContentForm(self.request.arguments)
        if not (recipient_form.validate() and bill_content_form.validate()):
            if not recipient_form.validate():
                logging.debug(u'Форма получателя не валидна.')
            if not bill_content_form.validate():
                logging.debug(u'Форма содержимого не валидна.')
            self.context.update({'title': u'Создание счёта',
                                 'module_name': url_base,
                                 'sender': RequisitesDB.get_one({'inn': '772160030650'}),
                                 'recipient': recipient_form,
                                 'bill_content': bill_content_form,
                                 'bill_num': Counter.next_key('bill'),
                                 'date': datetime.now(),
                                 })
            self.render(tmpl('create'))
        else:
            from units.documents import create_context, create_bill, create_pdf_bill
            
            req = RequisitesDB.create_from_data(recipient_form.data)
            contr = ContactorDB.create(self.user_id, req['_id'])['_id']
            items_from_form = bill_content_form.data['items']
            items = []
            for i in items_from_form:
                if i['count'] > 0.0 and i['name']:
                    items.append(i)
            cont = ContentDB.create(items)['_id']
            bill_num = Counter.next_key('bill')
            date = datetime.now()
            sender_user = UserDB.get_one({'id': 1})
            bill = BillDB.create_simple(sender_user['_id'], contr, cont, bill_num, date)
            
            context = create_context(RequisitesDB.get_by_id(sender_user['requisites']), 
                                     req, bill_num, date, items)
            
            self.write(create_bill(context))
            self.xsrf_token
            self.flush()
            create_pdf_bill(context, 'asdf.pdf')
            