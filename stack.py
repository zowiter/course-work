# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:44:22 2021

@author: eveli
"""

class Stack(object):
    def __init__(self):
        self.items = []

#Проверяет, пуст ли список, и возвращает истину или ложь.
    def isEmpty(self):
        if len(self.items) > 0:
            return False
        return True
    
#Очистка списка
    def clear(self):
        self.items = []
        
#Добавляет элементы в конец списка
    def push(self, item):
        self.items.append(item)
        
#Удаляет элементы из конца списка
    def pop(self):
        if not self.isEmpty():
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None
    
#Возвращает элемент в конец списка
    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]
        return None