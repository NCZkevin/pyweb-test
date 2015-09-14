# -*- coding: UTF-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from models import Student

class TestStudent(object):
    
    @classmethod
    def setUpClass(cls):
        global o1_id
        
        o1 = Student()
        o1.url_number = 1
        o1.public_profile.realname = '李小兵'
        o1.save()
        
        o1_id = o1.id
        
    def setUp(self):
        global o1_id
        self.o1_id = o1_id
        
        
        
        
        
