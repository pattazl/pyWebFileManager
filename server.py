#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bottle import run
import sys, os, time, urllib2, json

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))
import controllers
from config import config

run(host=config.host, port=config.port, reloader=True, debug=False)
