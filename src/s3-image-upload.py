#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    This is the s3-image-upload.py script for cloudControl's new architecture. With this
    file a user is enabled to upload a given file (a squashed image file) to S3.

    In order for this to work, the AWS credentials need to be set via environment variables!
    Make sure to set following environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

    Bug request to: Hans-Gunther Schmidt (hgs@cloudcontrol.com)
"""
import argparse
import os
import sys
import definitions
from libs3 import upload
from version import __version__
from definitions import CLOUDCONTROL_SQUASHFS_IMAGE_BUCKET


def parse_shell_parameters():
    """
        Parse the provided shell parameters
    """
    usage = '%(prog)s [-h, --help] [command]'
    description = '%(prog)s AWS S3 SquashFS Image uploader'
    epilog = "And now you're in control!"

    parser = argparse.ArgumentParser(description=description, epilog=epilog, usage=usage)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ver.{}'.format(__version__))
    parser.add_argument('-d', '--debug', action="store_true", default=False)
    parser.add_argument('-f', '--file', action='store', help="An (squashFS) image file to upload to S3",
        required=True)
    parser.add_argument('-k', '--key', action='store', help="The identifying key for this image in S3",
        required=True)
    parser.add_argument('-b', '--bucket', action='store', default=CLOUDCONTROL_SQUASHFS_IMAGE_BUCKET,
        help="A valid AWS S3 bucket (default: \"{}\")".format(CLOUDCONTROL_SQUASHFS_IMAGE_BUCKET))

    return parser.parse_args()


def main():
    """
        Run the whole thing
    """
    args = parse_shell_parameters()

    image_file = args.file
    bucket = args.bucket
    image_key = args.key
    definitions.DEBUGGING = args.debug

    if args.debug:
        print args

    if not os.path.isfile(image_file):
        sys.exit("{} is not a valid (image) file!".format(image_file))

    upload(image_file, image_key, bucket)


#
# MAIN
#
main()