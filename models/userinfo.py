# -*- coding: utf-8 -*-

from base import BaseDocument, connection
import datetime

@connection.register
class UserInfoDB(BaseDocument):
    
    __collection__ = 'userinfo'
    __title__ = u'Информация о юзере'
    
    skeleton = {
                    'name': unicode,
                    'avatar': unicode,
                    'about': unicode,
                    'city': unicode,
                    'male': unicode,
                    'date_birth': datetime.datetime,
                    'career': unicode,
                    
                    'twitter_link': unicode,
                    'youtube_link': unicode,
                    'instagram_link': unicode,
                    'linkedin_link': unicode,
                    'google_plus_link': unicode,
                    'facebook_link': unicode,
                    'skype_link': unicode,
                    'vk_link': unicode,
                }
    

    @staticmethod
    def create():
        a = connection.UserInfoDB()
        a.save() 
        return a
    
    def get_profile(self):
        res = dict(self)
        res['links'] = {}
        for k in res.keys():
            if k.endswith('_link'):
                if res[k]:
                    res['links'].update({k[:-5]: res[k]})
                del res[k]
        return res
    
    """ Вспомогательные функции для внутреннего использования """
    