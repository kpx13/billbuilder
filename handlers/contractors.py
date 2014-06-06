# -*- coding: utf-8 -*-
import logging

from tornado_routes import route

from basehandler import BaseHandler, authorized
from models.contactor import ContactorDB
from models.requisites import RequisitesDB
from forms.contractor import RequisitesForm, ContractorForm


url_base = 'contractors'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)

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
        
@route('create')
class ContractorsCreate(BaseHandler):
    _model = ContactorDB
    
    @authorized
    def get(self):
        self.context.update({'title': u'Создание контрагента',
                             'module_name': url_base,
                             'requisites_form': RequisitesForm(),
                             'contractor_form': ContractorForm(),
                             })
        self.render(tmpl('create'))
    
    
    def post(self, *args, **kwargs):
        requisites_form = RequisitesForm(self.request.arguments)
        
        if not requisites_form.validate():
            """ Не валидна форма реквизитов """
            if not requisites_form.validate():
                logging.debug(u'Форма реквизитов контрагента не валидна.')
            self.context.update({'title': u'Создание контрагента',
                                'module_name': url_base,
                                'requisites_form': requisites_form,
                                'contractor_form': ContractorForm(self.request.arguments),
                                    })
            self.render(tmpl('create'))
        else:
            req = RequisitesDB.create_from_data(requisites_form.data)
            contractor_data = self.request.arguments
            contractor_data.update({'user': [str(self.user_id)],
                                    'requisites': [str(req['_id'])]})
            print 'CONTRACTOR DATA'
            print contractor_data
            
            contractor_form = ContractorForm(contractor_data)
            
            if not contractor_form.validate():
                logging.error(u'С какого-то хуя форма контрагента не валидна: %s' % contractor_form.errors)
            
            con = ContactorDB.create_from_data(contractor_form.data)
            
            self.context.update({'title': u'Создание контрагента',
                                'module_name': url_base,
                                'requisites_form': requisites_form,
                                'contractor_form': contractor_form,
                                    })
            self.render(tmpl('create'))
            logging.debug(u'Контрагент сохранен.')

