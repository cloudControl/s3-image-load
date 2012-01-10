# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    Simplest logging facility!

    Bug request to: Hans-Gunther Schmidt (hgs@cloudcontrol.com)
"""

#TODO: Use real logger!


import definitions

def log(message):
    """
        Rudimentary logging
    """
    if definitions.DEBUGGING:
        print message

