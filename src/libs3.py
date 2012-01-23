# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    This is the s3-image-upload.py script for cloudControl's new architecture. With this
    file a user is enabled to upload a given file (a squashed image file) to S3.

    In order for this to work, the AWS credentials need to be set via environment variables!
    Make sure to set following environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

    s3-image-load is freely distributable under the terms of an MIT-style license. 
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
        bucket = s3.create_bucket(bucket_name)
        key = bucket.new_key(image_key)
        key.set_contents_from_filename(image_file)
    except boto.exception.S3CreateError as error:
        log.error("Could not create {}! Error: {}".format(image_key, error))
    except (boto.exception.S3DataError, boto.exception.S3PermissionsError, boto.exception.S3ResponseError) as error:
        log.error("Ran into boto.exception.S3DataError! Error: {}".format(error))
    except Exception as error:
        log.error("Unexpected error! Error: {}".format(error))
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
        log.error("Could not create {}! Error: {}".format(image_key, error))
    except (boto.exception.S3DataError, boto.exception.S3PermissionsError, boto.exception.S3ResponseError) as error:
        log.error("Ran into boto.exception.S3DataError! Error: {}".format(error))
    except Exception as error:
        log.error("Unexpected error! Error: {}".format(error))
        sys.exit(1)

    return 0
