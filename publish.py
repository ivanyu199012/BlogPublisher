
import argparse
import ntpath
from devTOPublisher import DevTOPublisher

from fileHandler import FileHandler

if __name__ == "__main__":
	# initialise parser
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

	# read arguments
	args = parser.parse_args()
	arg_dict = vars( args )
	print(f'{ arg_dict= }')

	file_basename = ntpath.basename( arg_dict["filepath"] )
	markdown_text, file_ext = FileHandler.read_file( arg_dict["filepath"] )

	# Publish to Dev To
	formatted_markdown_text = DevTOPublisher.format_markdown_text( markdown_text )
	req_data_dict = DevTOPublisher.prep_req_data_dict( arg_dict, formatted_markdown_text )
	dev_to_url = DevTOPublisher.post_article( req_data_dict )
	print(f'{ dev_to_url= }')
