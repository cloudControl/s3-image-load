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


    This is the s3-image-upload.py script for cloudControl's new
    architecture. With this file a user is enabled to upload a 
    given file (a squashed image file) to S3.

    In order for this to work, the AWS credentials need to be set 
    via environment variables! Make sure to set following 
    environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

"""

import argparse
import os
import sys
from ConfigurationHandler import ConfigurationHandler
from libs3 import upload, logger
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
    description = '%(prog)s AWS S3 SquashFS Image uploader'
    epilog = "And now you're in control!"

    parser = argparse.ArgumentParser(description=description, epilog=epilog, usage=usage)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ver.{0}'.format(__version__))
    parser.add_argument('-i', '--input', action='store', help="An (squashFS) image input file to upload to S3",
        required=True)
    parser.add_argument('-k', '--key', action='store', help="The identifying key for this image in S3",
        required=True)
    parser.add_argument('-b', '--bucket', action='store', default=config.get('S3', 'bucket'),
        help="A valid AWS S3 bucket (default: \"{0}\")".format(config.get('S3', 'bucket')))

    log.debug("Shell arguments: {0}".format(parser.parse_args()))

    return parser.parse_args()


def main():
    """
        Run the whole thing
    """
    # Get the shell arguments
    args = parse_shell_parameters()

    # Transfer shell arguments to variables
    image_file = args.input
    bucket = args.bucket
    image_key = args.key

    # Given image file is not a valid file? Hmm, that's a problem!
    if not os.path.isfile(image_file):
        log.error("{0} is not a valid (image) file!".format(image_file))
        sys.exit("{0} is not a valid (image) file!".format(image_file))

    # Ok, all set! We can upload the file ...
    log.debug('Uploading file: "{0}" with key: "{1}" to bucket: "{2}"'.format(image_file, image_key, bucket))
    upload(image_file, image_key, bucket)

    return 0


####################################################################
#
# MAIN
#
####################################################################

if __name__ == "__main__":
    log = logger.get_logger('s3-image-upload')
    config = ConfigurationHandler().read_configuration()
    main()
