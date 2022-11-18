#

import json
from publisher import Publisher
from configHandler import ConfigHandler
import requests

class DevTOPublisher( Publisher ):

	@classmethod
	def prep_req_data_dict(self, args, markdown_content) -> dict:
		articles_dict = {
			"title" : args[ "title" ],
			"body_markdown" :markdown_content,
			"published" : args['pub'] if "true" else "false",
			"canonicalUrl" : args['canonicalUrl'],
			"series" : args['series']
		}

		if args[ "imageUrl" ]:
			articles_dict["main_image"] = args["imageUrl"]

		if args[ "subtitle" ]:
			articles_dict["description"] = args["subtitle"]

		if args[ 'tags' ]:
			articles_dict['tags'] = [t.strip().replace( " ", "" ) for t in args['tags'].split(',')]

		return {
			"article" : articles_dict
		}

	@classmethod
	def post_article(self, req_data_dict) -> str:
		headers = {
			"Content-Type"	:"application/json",
			"api-key": ConfigHandler.get_dev_to_api_key(),
		}
		url = "https://dev.to/api/articles"
		response = requests.post(url, headers=headers, data=json.dumps( req_data_dict ))

		if response.status_code not in [201]:
			print(f'{ response.status_code= }')
			print(f'{ response.content= }')
			return None

		post_url = f'{response.json()["url"]}/edit'
		print(f'{ post_url= }')
		return post_url