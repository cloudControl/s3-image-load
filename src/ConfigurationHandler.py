# -*- coding: utf-8 -*-
"""
    Copyright 2010 cloudControl GmbH

    This is the ConfigurationHandler. You can manage all configuration for your applications
    by just creating a 'settings.cfg' file and putting all values into that config file.

    Bug request to: Hans-Gunther Schmidt (hgs@cloudcontrol.com)
"""

import ConfigParser
import os

class ConfigurationHandler(object):

    default_configuration_file_name = '{}/.s3_image_load.cfg'.format(os.path.expanduser('~'))

    default_config_set = {
        'Logging' : {
            'LOG_FILENAME'  : 's3-image-load.log',
            'LOG_DIRECTORY' : '/tmp/'
        },
        'S3' : {
            'BUCKET'        : 'images.squashfs.cloudcontrol.com'
        }
    }

    def write_default_configuration(self):
        """
            Create a default configuration file (if the default is non-existent or faulty)
        """
        config = ConfigParser.RawConfigParser()

        # Go through the sections
        for section in self.default_config_set.keys():
            config.add_section(section)

            # Go through each settings within a section
            for key in self.default_config_set[section].keys():
                config.set(section, key, self.default_config_set[section][key])

        with open(self.default_configuration_file_name, 'wb') as config_file:
            config.write(config_file)


    def read_configuration(self, configuration_file=None):
        """
            Read the configuration file
        """
        # Check if we have received a different configuration file name
        if configuration_file is None:
            configuration_file = self.default_configuration_file_name

        # Check if the file even exists! If not, we have to write a default configuration file.
        if not os.path.exists('./{0}'.format(configuration_file)):
            self.write_default_configuration()

        # Read the configuration file
        config = ConfigParser.RawConfigParser()
        config.read(configuration_file)

        return config
