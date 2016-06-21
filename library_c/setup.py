#!/usr/bin/env python

from setuptools import setup, find_packages, Extension

_blinkt = Extension(
	'_blinkt',
	include_dirs=['lib'],
	libraries=['bcm2835'],
	sources=['lib/blinkt.c','blinkt_wrap.c']
)

setup(
	name = 'blinkt_c',
	version = '0.0.1',
	author = "Philip Howard",
	author_email = "phil@pimoroni.com",
	url = "",
	description = "",
	long_description = "",
	ext_modules = [ _blinkt ],
	py_modules = ["blinkt"],
	install_requires = [],
	headers=['lib/blinkt.h']
)
