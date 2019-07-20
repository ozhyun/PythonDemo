#!/usr/bin/python

from ctypes import cdll

lib = cdll.LoadLibrary('./libapi.so')
lib.simple(50)

a = lib.sum(5, 6)
print(a)
