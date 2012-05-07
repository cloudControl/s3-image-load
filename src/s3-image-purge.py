#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.
"""
import argparse
from ConfigurationHandler import ConfigurationHandler
from libs3 import purge, logger
from version import __version__

####################################################################
#
# FUNCTIONS
#
####################################################################

def parse_shell_parameters():
    """
        Parse the provided shell parameters
    """
    usage = '%(prog)s [-h, --help] [command]'
    description = '%(prog)s AWS S3 SquashFS Image Downloader'
    epilog = "And now you're in control!"

    parser = argparse.ArgumentParser(description=description, epilog=epilog, usage=usage)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ver.{0}'.format(__version__))
    parser.add_argument('-p', '--prefix', help="The prefix for key search in S3", required=True)
    parser.add_argument('-b', '--bucket', default=config.get('S3', 'bucket'), help="A valid AWS S3 bucket (default: \"{0}\")".format(config.get('S3', 'bucket')))
    parser.add_argument('-l', '--leave-newest', dest='leave', help="Leave the 'n' newest in S3", type=int, default=10)

    log.debug("Shell arguments: {0}".format(parser.parse_args()))

    return parser.parse_args()


def main():
    """
        Run the whole thing
    """
    # Get the shell arguments
    args = parse_shell_parameters()

    # Transfer shell arguments to variables
    bucket = args.bucket
    prefix = args.prefix
    leave = args.leave

    log.debug('Purging with prefix: "{0}" from bucket: "{1}" leave: "{2}" images'.format(prefix, bucket, leave))
    purge(bucket, prefix, leave)

    return 0


####################################################################
#
# MAIN
#
####################################################################

if __name__ == "__main__":
    log = logger.get_logger('s3-image-download')
    config = ConfigurationHandler().read_configuration()
    main()
