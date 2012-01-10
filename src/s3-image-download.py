#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    In order for this to work, the AWS credentials need to be set via environment variables!
    Make sure to set following environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

    Bug request to: Hans-Gunther Schmidt (hgs@cloudcontrol.com)
"""
import argparse
import definitions
from libs3 import download
from version import __version__
from definitions import CLOUDCONTROL_SQUASHFS_IMAGE_BUCKET


def parse_shell_parameters():
    """
        Parse the provided shell parameters
    """
    usage = '%(prog)s [-h, --help] [command]'
    description = '%(prog)s AWS S3 SquashFS Image Downloader'
    epilog = "And now you're in control!"

    parser = argparse.ArgumentParser(description=description, epilog=epilog, usage=usage)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ver.{}'.format(__version__))
    parser.add_argument('-d', '--debug', action="store_true", default=False)
    parser.add_argument('-o', '--output', action='store', help="Output file (under which to store the S3 object)",
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

    destination_file = args.output
    bucket = args.bucket
    image_key = args.key
    definitions.DEBUGGING = args.debug

    if definitions.DEBUGGING:
        print args

    download(destination_file, image_key, bucket)


#
# MAIN
#
main()