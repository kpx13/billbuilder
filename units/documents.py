# -*- coding: utf-8 -*-

from settings import jinja_env
import pytils

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
    jinja_env.get_template(template_name).render(context)

