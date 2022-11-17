#
import re


class GistCodeUploader:

	DELIMITER = "_@_"
	LANG_KEY = "LANGUAGE"
	CODE_BLOCK_KEY = "CODE_BLOCK"

	@classmethod
	def exec(self, path):
		content = self.read_file(path)
		self.convert_code_block_to_id(content)

	@classmethod
	def read_file(self, path):
		content = None
		with open(path, 'r', encoding='utf-8') as f:
			content = f.read()
		return content

	@classmethod
	def convert_code_block_to_id(self, file_base_name, markdown_text):
		id_2_code_block_info_dict = {}

		temp_markdown_text = markdown_text
		code_block_arr = re.findall('```[\s\S][^```]+```', markdown_text)
		for index, code_block in enumerate(code_block_arr):
			id = f'{self.DELIMITER}{file_base_name}_code_{index}{self.DELIMITER}'
			temp_markdown_text = temp_markdown_text.replace(code_block, id)

			language = None
			if re.search( '```(.*)\n', code_block ):
				language = re.search( '```(.*)\n', code_block ).group( 0 ).replace( '```', '' ).replace( '\n', '' )

			pure_code_block = re.sub('```.*\n', '', code_block)
			pure_code_block = re.sub('```', '', pure_code_block)

			id_2_code_block_info_dict[id] = {
				self.LANG_KEY : language,
				self.CODE_BLOCK_KEY : pure_code_block
			}

		return id_2_code_block_info_dict, temp_markdown_text

	@classmethod
	def save_temp_markdown_file(self, temp_markdown_text):
		path = None
		return path

	@classmethod
	def upload_code_block_to_gist(self, id_2_code_block_info_dict):
		id_2_gist_link_dict = {}

		return id_2_gist_link_dict
