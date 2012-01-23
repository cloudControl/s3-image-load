# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    This is the LogHandler. This class provides easy means of logging to a file.

    s3-image-load is freely distributable under the terms of an MIT-style license. 
"""

import logging

class LogHandler(object):
    log_levels   = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

    logger       = 'default'
    log_format   = '%(asctime)-15s %(name)s %(levelname)s %(message)s'
    log_dir      = '/tmp/'
    log_filename = '{0}.log'.format(logger)


    def __init__(self, log_filename=None):
        """
            Initialize LogHandler
        """
        super(LogHandler, self).__init__()

        if log_filename is None:
            log_filename = self.log_filename

        self.log_formatter = logging.Formatter(self.log_format)
        self.log_file      = '{0}/{1}'.format(self.log_dir, log_filename)
        self.log_handler   = logging.FileHandler(self.log_file)
        self.log_handler.setFormatter(self.log_formatter)


    def get_logger(self, logger=None):
        """
            Create the logger object and return it back
        """
        if logger is None:
            logger = self.logger

        log = logging.getLogger(logger)
        log.addHandler(self.log_handler)
        log.setLevel(logging.DEBUG)

        return log
