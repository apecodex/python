# -*- coding: utf-8 -*-

import functools

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			print("call %s %s()" % (text,func.__name__))
			s = func(*args,**kw)
			print("end feel")
			return s
		return wrapper
	return decorator


@log("text")
def now():
		print("2016-9-28")

now()

print(now.__name__)