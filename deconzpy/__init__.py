#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.9.1"
__author__ = "balu-"
__url__ = "https://github.com/balu-/deconzpy"

""" Router

	the Router is a Singelton object, 
	that builds the entry-point to all the other elements.
	It further manages updates delivered via webservice, 
	updates elements & triggers observers accordingly
"""
from .Router import Router
