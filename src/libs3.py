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
"""

import sys
import boto
from boto.s3.connection import S3Connection
from LogHandler import LogHandler
from nodecontroller.config import get_aws_s3_credentials

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

    credentials = get_aws_s3_credentials()
    try:
        conn = S3Connection(credentials['aws_access_key'], credentials['aws_secret_key'])
        log.debug(">>> Connected to S3")
    except boto.exception.NoAuthHandlerFound:
        sys.exit("Could not find valid AWS credentials! Make sure to set \'AWS_ACCESS_KEY_ID\' and "
                 "\'AWS_SECRET_ACCESS_KEY\'!")
    return conn


def upload(image_file, image_key, bucket_name):
    """
        Upload a given image file to our S3 bucket
    """
    log = logger.get_logger("upload")

    try:
        s3 = connect()
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

def purge(bucket_name, prefix, leave):
    """
        Upload a given image file to our S3 bucket
    """
    log = logger.get_logger("download")

    keys = []
    try:
        s3 = connect()
        keys = s3.get_bucket(bucket_name).get_all_keys(prefix=prefix)
    except (boto.exception.StorageResponseError) as error:
        log.error("Ran into boto.exception.StorageResponseError! Error: {0}".format(error))
    except Exception as error:
        log.error("An undefined error occured! Error: {0}".format(error))
        sys.exit(1)

    if not len(keys):
        return

    def sort_keys(key1, key2):
        # compare the datetime objects from boto
        ts1 = boto.utils.parse_ts(key1.last_modified)
        ts2 = boto.utils.parse_ts(key2.last_modified)
        if ts2 > ts1: return 1
        if ts2 < ts1: return -1
        return 0

    to_delete = sorted(keys, cmp=sort_keys)[leave:]
    for key in to_delete:
        try:
            key.delete()
        except boto.exception.BotoServerError, error:
            log.error("Image with key {0} could not removed on server! Error: {1}".format(key, error))
        except Exception, error:
            log.error("An undefined error occured! key: {0}, error {1}".format(key, error))
            break

    return to_delete
