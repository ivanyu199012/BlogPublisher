#
from fileHandler import FileHandler
from gistCodeHandler import GistCodeHandler

if __name__ == "__main__":

	gist_id_list = FileHandler.read_json_file_2_dict( "temp/gist_id_list.json" )
	GistCodeHandler.delete_gists( gist_id_list )
