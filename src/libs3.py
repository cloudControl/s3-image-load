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

    In order for this to work, the AWS credentials need to be 
    set via environment variables! Make sure to set following 
    environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

"""

import sys
import boto
from LogHandler import LogHandler

####################################################################
#
# GLOBALS
#
####################################################################

# Logger with given log file name (placed in /tmp/)
logger = LogHandler(log_filename='s3-image-load.log')


####################################################################
#
# FUNCTIONS
#
####################################################################

def connect():
    """
        Connect to S3 with credentials
    """
    log = logger.get_logger("connect")

    try:
        s3 = boto.connect_s3()
        log.debug(">>> Connected to S3")
    except boto.exception.NoAuthHandlerFound:
        sys.exit("Could not find valid AWS credentials! Make sure to set \'AWS_ACCESS_KEY_ID\' and "
                 "\'AWS_SECRET_ACCESS_KEY\'!")
    return s3


def upload(image_file, image_key, bucket_name):
    """
        Upload a given image file to our S3 bucket
    """
    log = logger.get_logger("upload")

    try:
        s3 = connect()
        bucket = s3.get_bucket(bucket_name)
        if not bucket_name in s3.get_all_buckets():
            bucket = s3.create_bucket(bucket_name)

        key = bucket.new_key(image_key)
        key.set_contents_from_filename(image_file)
    except boto.exception.S3CreateError as error:
        log.error("Could not create {0}! Error: {1}".format(image_key, error))
    except (boto.exception.S3DataError, boto.exception.S3PermissionsError, boto.exception.S3ResponseError) as error:
        log.error("Ran into boto.exception.S3DataError! Error: {0}".format(error))
    except Exception as error:
        log.error("Unexpected error! Error: {0}".format(error))
        sys.exit(1)

    return 0


def download(destination_file, image_key, bucket_name):
    """
        Upload a given image file to our S3 bucket
    """
    log = logger.get_logger("download")

    try:
        s3 = connect()
        key = s3.get_bucket(bucket_name).get_key(image_key)
        key.get_contents_to_filename(destination_file)
    except boto.exception.S3CreateError as error:
        log.error("Could not create {0}! Error: {1}".format(image_key, error))
    except (boto.exception.S3DataError, boto.exception.S3PermissionsError, boto.exception.S3ResponseError) as error:
        log.error("Ran into boto.exception.S3DataError! Error: {0}".format(error))
    except Exception as error:
        log.error("Unexpected error! Error: {0}".format(error))
        sys.exit(1)

    return 0
