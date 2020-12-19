#-*- coding: utf-8 -*-

class Memory(dict):#{}형이라 엑세스 용의

    def __init__(s):
        pass

    #기본 자료형 상속
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        if 
        return self.__setitem__(attr, value)

    def __delattr__(self, attr):
        return self.__delitem__(attr)
    
