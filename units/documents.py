# -*- coding: utf-8 -*-

from settings import jinja_env
import pytils
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO

"""
    items: список из {
                            'name': 'наименование',     # str
                            'unit': 'ед. изм.',        # str
                            'count': 'кол-во',        # float/int
                            'price': 'сумма',        # float
                        }
"""

def get_sum(items):
    return sum([x['count']*x['price'] for x in items])

def create_context(sender, recipient, bill_num, date, items):
    u"sender, recipient - объекты отправителя (его акк) и получателя, номер счёта, дата и список наименований"
    return {
                'sender': sender,
                'recipient': recipient,
                'bill_num': bill_num,
                'date': date,
                'items': items,
                'items_count': len(items),
                'items_sum': get_sum(items),
                'items_sum_text': pytils.numeral.rubles(get_sum(items)).capitalize(),
            }

def create_bill(context, template_name='documents/bill.html'):
    return jinja_env.get_template(template_name).render(context)

def create_pdf_bill(context, filename, template_name='documents/bill_pdf.html'):
    context['MEDIA_ROOT'] = '/home/kpx/billbuilder/billbuilder'
    html = jinja_env.get_template(template_name).render(context)
    result = StringIO.StringIO()
    pisa.pisaDocument(StringIO.StringIO(html.encode('utf-8')), result, show_error_as_pdf=True, encoding='UTF-8')
    open(filename, 'wb').write(result.getvalue())    
