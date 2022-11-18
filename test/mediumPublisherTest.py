#

import ntpath
import os
import sys
import unittest


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from gistCodeHandler import GistCodeHandler
from customParser import CustomParser
from fileHandler import FileHandler
from mediumPublisher import MediumPublisher

class DevTOPublisherTest( unittest.TestCase ) :

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		file_path = "temp/Django_background_task.md"
		self.file_basename = ntpath.basename( file_path )
		self.markdown_text, self.file_ext = FileHandler.read_file( file_path )

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

		arg_dict = vars( args )
		arg_dict[ "contentFormat" ] = self.file_ext
		temp_markdown_text, id_2_gist_link_dict = GistCodeHandler.convert_blog_code_2_gists( self.file_basename, self.markdown_text )
		# gist_id_list = [ gist_link.replace( "https://gist.github.com/", "" ) for gist_link in id_2_gist_link_dict.values() ]
		# GistCodeHandler.delete_gists( gist_id_list )
		temp_markdown_text = MediumPublisher.format_markdown_text( temp_markdown_text, id_2_gist_link_dict  )
		req_data_dict = MediumPublisher.prep_req_data_dict( arg_dict, temp_markdown_text)
		for key in ["title", "content", "contentFormat"]:
			self.assertEqual( key in req_data_dict, True)

		FileHandler.write_obj_2_json_file( "req_data_dict", req_data_dict )

	def test_1_post_article( self ):
		req_data_dict = FileHandler.read_json_file_2_dict( "temp/req_data_dict.json" )
		url = MediumPublisher.post_article( req_data_dict )
		print(f'{ url= }')

if __name__ == '__main__':
	unittest.main()
