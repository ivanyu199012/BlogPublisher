#
class GistCodeUploader:

	@classmethod
	def read_file( self, path ):
		content = None
		with open( path, 'r', encoding='utf-8') as f:
			content = f.read()
		return content

	@classmethod
	def convert_code_block_to_id( self, markdown_text ):
		id_2_code_block_info_dict = {}

		return

	@classmethod
	def save_temp_markdown_file( self, temp_markdown_text ):
		path = None
		return path

	@classmethod
	def upload_code_block_to_gist( self, id_2_code_block_info_dict ):
		id_2_gist_link_dict = {}

		return id_2_gist_link_dict