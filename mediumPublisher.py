
import json
from configHandler import ConfigHandler
from publisher import Publisher
import requests

class MediumPublisher(Publisher):

	HEADERS = {
		"Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding"	:"gzip, deflate, br",
		"Accept-Language"	:"en-US,en;q=0.5",
		"Connection"	:"keep-alive",
		"Host"	:"api.medium.com",
		"Authorization": f"Bearer {ConfigHandler.get_medium_token()}",
		"Upgrade-Insecure-Requests":	"1",
		"User-Agent":	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
	}

	@classmethod
	def format_markdown_text( self, markdown_content : str, id_2_gist_link_dict : dict = None  ) -> str:
		for id, gist_link in id_2_gist_link_dict.items():
			markdown_content = markdown_content.replace( id, f"\n{ gist_link }\n" )
		return markdown_content

	@classmethod
	def prep_req_data_dict(self, args, markdown_content) -> dict:
		'''prepares payload to publish post'''
		content_format = "markdown" if args[ 'contentFormat' ] == 'md' else args[ 'contentFormat' ]
		data = {
			"title": args['title'],
			"content": markdown_content,
			"contentFormat": content_format,
		}

		if args['tags']:
			data['tags'] = [t.strip() for t in args['tags'].split(',')]

		data['canonicalUrl'] = args[ 'canonicalUrl' ] if args[ 'canonicalUrl' ] else None
		data['publishStatus'] = args['pub'] if args['pub'] else 'draft'
		return data

	@classmethod
	def post_article(self, req_data_dict) -> str:
		'''posts an article to medium with the input payload'''
		author_id = self.__get_author_id()
		url = f"https://api.medium.com/v1/users/{author_id}/posts"
		response = requests.post(url, headers=self.HEADERS, data=req_data_dict)
		if response.status_code not in [200, 201]:
			print(f'{ response.status_code= }')
			print(f'{ response.content= }')
			return None

		response_json = response.json()
		# get URL of uploaded post
		pub_url = response_json["data"]["url"]
		return pub_url

	@classmethod
	def __get_author_id( self ):
		'''uses the /me medium api endpoint to get the user's author id'''
		response = requests.get("https://api.medium.com/v1/me", headers=self.HEADERS, params={"Authorization": f"Bearer {ConfigHandler.get_medium_token()}" })

		if response.status_code not in [200]:
			print(f'{ response.status_code= }')
			print(f'{ response.content= }')
			return None

		return response.json()['data']['id']