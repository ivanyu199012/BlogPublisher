#
import  unittest

from gistCodeUploader import GistCodeUploader

class GistCodeUploaderTest( unittest.TestCase ) :

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )


	def test_read_file( self ):
		content = GistCodeUploader.read_file( "temp/Django_background_task.md" )
		self.assertEqual( "Introduction" in content, True )
		print(f'{ content= }')

if __name__ == '__main__':
	unittest.main()