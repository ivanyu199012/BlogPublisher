#

import argparse


class CustomParser:

	@staticmethod
	def create_parser():
		parser = argparse.ArgumentParser()

		# add compulsory arguments
		parser.add_argument('filepath') # positional argument
		parser.add_argument('-t', '--title', required=True, help="title of post", type=str) # named argument
		parser.add_argument('-cUrl', '--canonicalUrl', required=True, help="Canonical Url", type=str) # named argument
		parser.add_argument('--series', required=True, help="Series", type=str)

		# add compulsory arguments
		parser.add_argument('-a', '--tags', required=False, help="tags, separated by ,", type=str)
		parser.add_argument('-p', '--pub', required=False, help="publish status, one of draft/unlisted/public, defaults to draft", type=str, choices=["public", "unlisted", "draft"])
		parser.add_argument('--imageUrl', required=False, help="Image URL", type=str)
		parser.add_argument('--subtitle', required=False, help="Subtitle", type=str)

		return parser