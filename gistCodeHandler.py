#
import json
import ntpath
import re
import requests
from configHandler import ConfigHandler
from fileHandler import FileHandler


class GistCodeHandler:

	DELIMITER = "_@_"
	LANG_KEY = "LANGUAGE"
	CODE_BLOCK_KEY = "CODE_BLOCK"
	LANG_2_FILE_EXT = {
		"python" : "py",
		"javascript" : "js"
	}
	HEADERS = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {ConfigHandler.get_github_token()}",
	}

	@classmethod
	def convert_blog_code_2_gists(self, file_basename, content):
		id_2_code_block_info_dict, temp_markdown_text = self.convert_code_block_to_id( file_basename, content )
		id_2_gist_link_dict = self.upload_code_block_to_gist( id_2_code_block_info_dict )
		return temp_markdown_text, id_2_gist_link_dict

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
		id_2_gist_link_dict = {}
		for id, code_block_info_dict in id_2_code_block_info_dict.items():
			filename = id.replace( self.DELIMITER, "" ) + f".{ self.LANG_2_FILE_EXT[ code_block_info_dict[ self.LANG_KEY ] ] }"
			data_dict = {
				"description": id.replace( self.DELIMITER, "" ),
				"public": "true",
				"files":{ filename:{ "content" : code_block_info_dict[ self.CODE_BLOCK_KEY ] }}
			}
			response = requests.post("https://api.github.com/gists", headers=self.HEADERS, data=json.dumps(data_dict))

			if response.status_code not in [200, 201]:
				print(f'{ response.status_code= }')
				print(f'{ response.content= }')
				return None

			id_2_gist_link_dict[ id ] = response.json()["html_url"]
			print( f"{ id = }, { id_2_gist_link_dict[ id ] = }" )

		return id_2_gist_link_dict

	@classmethod
	def delete_gists( self, gist_id_list ):
		for gist_id in gist_id_list:
			response = requests.delete(f"https://api.github.com/gists/{gist_id}", headers=self.HEADERS )

			if response.status_code not in [204]:
				print(f'{ response.status_code= }')
				print(f'{ response.content= }')
				return None

			print( f"Delete Gist #{gist_id} successfully." )
