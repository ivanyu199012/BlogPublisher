#
import re
import ntpath


class GistCodeUploader:

	DELIMITER = "_@_"

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
			id_2_code_block_info_dict[id] = code_block

		return id_2_code_block_info_dict, temp_markdown_text

	@classmethod
	def save_temp_markdown_file(self, temp_markdown_text):
		path = None
		return path

	@classmethod
	def upload_code_block_to_gist(self, id_2_code_block_info_dict):
		id_2_gist_link_dict = {}

		return id_2_gist_link_dict
