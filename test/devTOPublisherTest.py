#

import os
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from customParser import CustomParser
from fileHandler import FileHandler
from devTOPublisher import DevTOPublisher

class DevTOPublisherTest( unittest.TestCase ) :

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		markdown_text, _ = FileHandler.read_file( "temp/Django_background_task.md" )
		self.markdown_text = DevTOPublisher.format_markdown_text( markdown_text )

	def test_0_prep_req_data_dict( self ):
		parser = CustomParser.create_parser()
		args = parser.parse_args( [
			"temp\\Django_background_task.md",
			"-t",
			"A simple approach for background task in Django_v1",
			"--series",
			"Python",
			"--canonicalUrl",
			"https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django",
			"--imageUrl",
			"https://ivanyu2021.hashnode.dev/_next/image?url=https%3A%2F%2Fcdn.hashnode.com%2Fres%2Fhashnode%2Fimage%2Funsplash%2FaOC7TSLb1o8%2Fupload%2Fv1668391959346%2FDUaEL91q3w.jpeg%3Fw%3D1600%26h%3D840%26fit%3Dcrop%26crop%3Dentropy%26auto%3Dcompress%2Cformat%26format%3Dwebp&w=1920&q=75",
			"--tags",
			"Python,Django,Threads, Message Queue"
		 ] )

		req_data_dict = DevTOPublisher.prep_req_data_dict( vars( args ), self.markdown_text )
		self.assertEqual( "article" in req_data_dict, True )

		FileHandler.write_obj_2_json_file( "req_data_dict", req_data_dict )

	def test_1_post_article( self ):
		req_data_dict = FileHandler.read_json_file_2_dict( "temp/req_data_dict.json" )

		url = DevTOPublisher.post_article( req_data_dict )
		self.assertEqual( "https://dev.to/ivanyu2021/" in url, True )

if __name__ == '__main__':
	unittest.main()
