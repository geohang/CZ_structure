import pymake

pm = pymake.Pymake()
pm.srcdir = './src'
pm.target = 'mf6'
pm.include_subdirs = True
pm.build()