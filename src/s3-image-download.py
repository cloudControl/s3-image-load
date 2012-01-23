# -*- coding: utf-8 -*-
"""
    Copyright 2011 cloudControl GmbH

    In order for this to work, the AWS credentials need to be set via environment variables!
    Make sure to set following environment variables:

        $ export AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
        $ export AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>

    s3-image-load is freely distributable under the terms of an MIT-style license. 
"""
import argparse
from ConfigurationHandler import ConfigurationHandler
from libs3 import download, logger
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

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ver.{}'.format(__version__))
    parser.add_argument('-o', '--output', action='store', help="Output file (under which to store the S3 object)",
        required=True)
    parser.add_argument('-k', '--key', action='store', help="The identifying key for this image in S3",
        required=True)
    parser.add_argument('-b', '--bucket', action='store', default=config.get('S3', 'bucket'),
        help="A valid AWS S3 bucket (default: \"{}\")".format(config.get('S3', 'bucket')))

    log.debug("Shell arguments: {}".format(parser.parse_args()))

    return parser.parse_args()


def main():
    """
        Run the whole thing
    """
    # Get the shell arguments
    args = parse_shell_parameters()

    # Transfer shell arguments to variables
    destination_file = args.output
    bucket = args.bucket
    image_key = args.key

    # Ok, all set! We can download the file ...
    log.debug('Downloading with key: "{}" from bucket: "{}" to output file: "{}" '.format(image_key, bucket,
        destination_file))
    download(destination_file, image_key, bucket)

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
