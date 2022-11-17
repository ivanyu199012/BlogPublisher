#
import ntpath
import  unittest

from gistCodeUploader import GistCodeUploader

class GistCodeUploaderTest( unittest.TestCase ) :

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )


	def test_read_file( self ):
		content = GistCodeUploader.read_file( "temp/Django_background_task.md" )
		self.assertEqual( "Introduction" in content, True )

	def test_convert_code_block_to_id( self ):
		file_path = "temp/Django_background_task.md"
		content = GistCodeUploader.read_file( file_path )
		file_basename = ntpath.basename( file_path )
		id_2_code_block_info_dict, temp_markdown_text = GistCodeUploader.convert_code_block_to_id( file_basename, content )

		for id in id_2_code_block_info_dict:
			self.assertEqual( file_basename in id, True )
			code_block_info_dict = id_2_code_block_info_dict[ id ]
			self.assertEqual( code_block_info_dict[ GistCodeUploader.LANG_KEY ], "python" )
			self.assertEqual( id in temp_markdown_text, True )




if __name__ == '__main__':
	unittest.main()