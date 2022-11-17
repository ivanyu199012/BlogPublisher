#

import configparser


class ConfigHandler:

	config = configparser.ConfigParser()
	config.read("tokens.ini")
	config_dict = config[ 'DEFAULT' ]

	@classmethod
	def get_github_token( self ):
		return self.config_dict[ "GITHUB_TOKEN" ]

