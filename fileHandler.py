

import json


class FileHandler:

	@classmethod
	def read_file( self, filepath):
		'''reads file from input filepath and returns a dict with the file content and contentFormat for the publish payload'''
		content = None
		with open(filepath, 'r', encoding='utf-8') as f:
			content = f.read()

		if filepath.find('.') < 0:
			return content, ""

		file_ext = filepath[ filepath.find(".")+1: ]
		return content, file_ext

	@classmethod
	def write_obj_2_json_file( self, filename_no_ext, obj ):
		with open( f"temp\{ filename_no_ext }.json", "w" ) as f:
			json.dump( obj, f, indent=4)

	@classmethod
	def read_json_file_2_dict( self, filepath ) -> dict:
		with open( filepath, "r", encoding='utf-8' ) as f:
			return json.load( f )
