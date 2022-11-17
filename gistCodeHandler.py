#
import json
import re
import requests
from configHandler import ConfigHandler


class GistCodeHandler:

	DELIMITER = "_@_"
	LANG_KEY = "LANGUAGE"
	CODE_BLOCK_KEY = "CODE_BLOCK"
	LANG_2_FILE_EXT = {
		"python" : "py",
		"javascript" : "js"
	}

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
	def save_file(self, filename_with_ext, text):
		path = f"temp/temp_{filename_with_ext}"

		with open(path, 'w', encoding='utf-8') as f:
			f.write( text )

		return path

	@classmethod
	def upload_code_block_to_gist( self, id_2_code_block_info_dict : dict ):
		headers = {
			"Accept": "application/vnd.github+json",
			"Authorization": f"Bearer {ConfigHandler.get_github_token()}",
		}

		id_2_gist_link_dict = {}
		for id, code_block_info_dict in id_2_code_block_info_dict.items():
			filename = id.replace( self.DELIMITER, "" ) + f".{ self.LANG_2_FILE_EXT[ code_block_info_dict[ self.LANG_KEY ] ] }"
			data_dict = {
				"description": id.replace( self.DELIMITER, "" ),
				"public": "false",
				"files":{ filename:{ "content" : code_block_info_dict[ self.CODE_BLOCK_KEY ] }}
			}
			response = requests.post("https://api.github.com/gists", headers=headers, data=json.dumps(data_dict))

			if response.status_code not in [200, 201]:
				print(f'{ response.status_code= }')
				print(f'{ response.content= }')
				return None

			id_2_gist_link_dict[ id ] = response.json()["html_url"]
			print( f"{ id = }, { id_2_gist_link_dict[ id ] = }" )

		return id_2_gist_link_dict