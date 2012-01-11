S3 SquashFS Image up-/downloader
================================
This is the s3-image-load repository. The set of scripts provide methods to upload given SquashFS image files (or any other file) to S3 and re-download those files again.

Requirements
------------
 * `boto` : [Boto on Google Code](http://code.google.com/p/boto/)
 * [Amazon AWS](http://aws.amazon.com/) Credentials (Access Key & Secret Key)


Setup
-----
1. Clone this project

2. Add cloned repository to your path, e.g.:

        $ export PATH=$PATH:<repository>

3. Make sure to add your AWS credentials to **either one** of following:

	1. [BotoConfig](http://code.google.com/p/boto/wiki/BotoConfig)

	2. Shell variables:

			$ export AWS_ACCESS_KEY_ID="_your_AWS_Access_Key_ID_"
			$ export AWS_SECRET_ACCESS_KEY="_your_AWS_Secret_Access_Key_"


Quick Start
-----------
Here is a quick description:

	$ ls -l *pdf
      -rw-r--r--  1 hgschmidt  staff  3200853 10 Jan 18:44 input.pdf
	$ file input.pdf
      input.pdf: PDF document, version 1.6
	$ s3-image-upload -k example_upload_key -f input.pdf
	$ s3-image-download -k example_upload_key -o output.pdf
	$ file *pdf
      input.pdf:  PDF document, version 1.6
      output.pdf: PDF document, version 1.6
	$


How to use the s3-image-loaders?
--------------------------------
There are currently two scripts to use:

 * **s3-image-upload**

    `s3-image-upload` will upload any given file for you, identified by a key provided by you, on Amazon S3.

        $ s3-image-upload --key <key> --file <input_filename>

	e.g.

		$ s3-image-upload --key an_example_key --file webstack.img

 * **s3-image-downlaod**

    `s3-image-download` will download an existing file on Amazon S3, given the case you have provided the correct key.

        $ s3-image-download --key <key> --output <output_filename>

    e.g.

        $ s3-image-download --key an_example_key --output webstack-download.img


Usage
-----
Here is the usage from `s3-image-download`:

	usage: s3-image-download.py [-h, --help] [command]

	s3-image-download.py AWS S3 SquashFS Image Downloader

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         show program's version number and exit
	  -d, --debug
	  -o OUTPUT, --output OUTPUT
	                        Output file (under which to store the S3 object)
	  -k KEY, --key KEY     The identifying key for this image in S3
	  -b BUCKET, --bucket BUCKET
	                        A valid AWS S3 bucket (default:
	                        "images.squashfs.cloudcontrol.com")

	And now you're in control!


And here is the usage from `s3-image-upload`:


    usage: s3-image-upload.py [-h, --help] [command]

    s3-image-upload.py AWS S3 SquashFS Image uploader

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -d, --debug
      -f FILE, --file FILE  An (squashFS) image file to upload to S3
      -k KEY, --key KEY     The identifying key for this image in S3
      -b BUCKET, --bucket BUCKET
                            A valid AWS S3 bucket (default:
                            "images.squashfs.cloudcontrol.com")

    And now you're in control!

Notes
-----
(c) 2011 cloudControl GmbH