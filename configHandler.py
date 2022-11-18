#

import configparser


class ConfigHandler:

	config = configparser.ConfigParser()
	config.read("tokens.ini")
	config_dict = config[ 'DEFAULT' ]

	@classmethod
	def get_github_token( self ):
		return self.config_dict[ "GITHUB_TOKEN" ]

	@classmethod
	def get_dev_to_api_key( self ):
		return self.config_dict[ "DEV_TO_TOKEN" ]

