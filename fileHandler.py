

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
		if file_ext == "md":
			file_ext = "markdown"

		return content, file_ext