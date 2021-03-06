# -*- coding: utf-8 -*-
import re
from tornado.escape import to_unicode
from wtforms import Form as WTForm
from wtforms import BooleanField, SelectMultipleField, Field, StringField
from wtforms.validators import StopValidation

class SwitchField(BooleanField):
    pass

class CheckboxesField(SelectMultipleField):
    pass

class TagsField(Field):
    
    def process(self, formdata, data=None):
        if formdata:
            hidden = []
            in_input = []
            for k in formdata.keys():
                if k.startswith('hidden-'):
                    hidden = formdata[k][0].split(',')
                elif k.endswith(self.name):
                    in_input = formdata[k]
                    
            data = list(set([x for x in in_input + hidden if x]))
            self.data = data
            return self.data
        elif data:
            #self.data = ','.join(data)
            self.data = data
        else:
            self.data = []
            
class CategoryField(Field):
    
    def pre_validate(self, form):
        if self.data == 'None':
            raise StopValidation(u'Обязательное поле.')
        
class TextEditorField(StringField):
    pass
        

class ModelNotProvidedException(Exception):
    pass


class TornadoArgumentsWrapper(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def getlist(self, key):
        try:
            values = []
            for v in self[key]:
                v = to_unicode(v)
                if isinstance(v, unicode):
                    v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
                values.append(v)
            return values
        except KeyError:
            raise AttributeError
        
class DBArgumentsWrapper(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def getlist(self, key):
        try:
            values = []
            for v in self[key]:
                v = to_unicode(v)
                if isinstance(v, unicode):
                    v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
                values.append(v)
            return values
        except KeyError:
            raise AttributeError

class Form(WTForm):
    def get_err_msg(self, err_code):
        text_errors = getattr(self, 'text_errors', {})
        return text_errors.get(err_code, err_code)

    def set_field_error(self, field_name, err_code):
        err_msg = self.get_err_msg(err_code)
        getattr(self, field_name).errors.append(err_msg)

    def set_nonfield_error(self, err_code):
        err_msg = self.get_err_msg(err_code)
        if self._errors is None:
            self._errors = {}
        self._errors.set_default('whole_form', [])
        self.errors['whole_form'].append(err_msg)
        getattr(self, 'field_name').errors.append(err_msg)
        
    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoArgumentsWrapper(formdata)
        if obj is not None:
            obj = DBArgumentsWrapper(obj)

        super(Form, self).process(formdata, obj, **kwargs)
