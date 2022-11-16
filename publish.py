import requests
import argparse
import subprocess

### ADD MEDIUM INTEGRATION TOKEN HERE ###


class MediumPublisher:

	TOKEN = None
	with open("token.ini", "r") as f:
		TOKEN = f.read()

	@classmethod
	def __get_header( self ):
		return  {
			"Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Encoding"	:"gzip, deflate, br",
			"Accept-Language"	:"en-US,en;q=0.5",
			"Connection"	:"keep-alive",
			"Host"	:"api.medium.com",
			"Authorization": f"Bearer {self.TOKEN}",
			"Upgrade-Insecure-Requests":	"1",
			"User-Agent":	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
		}

	@classmethod
	def read_file( self, filepath):
		'''reads file from input filepath and returns a dict with the file content and contentFormat for the publish payload'''
		content = None
		with open(filepath, 'r', encoding='utf-8') as f:
			content = f.read()

		if filepath.find('.') < 0:
			return {"content": content, "contentFormat": ""}

		file_ext = filepath[ filepath.find(".")+1: ]
		if file_ext == "md":
			file_ext = "markdown"
		return {"content": content, "contentFormat": file_ext}

	@classmethod
	def prep_data(self, args):
		'''prepares payload to publish post'''
		data = {
			"title": args['title'],
		}

		data = {**data, **self.read_file(args['filepath'])}
		if args['tags']:
			data['tags'] = [t.strip() for t in args['tags'].split(',')]

		data['publishStatus'] = args['pub'] if args['pub'] else 'draft'
		return data

	@classmethod
	def get_author_id( self ):
		'''uses the /me medium api endpoint to get the user's author id'''
		response = requests.get("https://api.medium.com/v1/me", headers=self.__get_header(), params={"Authorization": f"Bearer {self.TOKEN}" })
		if response.status_code == 200:
			return response.json()['data']['id']
		return None

	@classmethod
	def post_article(self, data):
		'''posts an article to medium with the input payload'''
		author_id = self.get_author_id()
		url = f"https://api.medium.com/v1/users/{author_id}/posts"
		response = requests.post(url, headers=self.__get_header(), data=data)
		if response.status_code not in [200, 201]:
			return None

		response_json = response.json()
		# get URL of uploaded post
		pub_url = response_json["data"]["url"]
		return pub_url

if __name__ == "__main__":
	# initialise parser
	parser = argparse.ArgumentParser()

	# add compulsory arguments
	parser.add_argument('filepath') # positional argument
	parser.add_argument('-t', '--title', required=True, help="title of post", type=str) # named argument

	# add compulsory arguments
	parser.add_argument('-a', '--tags', required=False, help="tags, separated by ,", type=str)
	parser.add_argument('-p', '--pub', required=False, help="publish status, one of draft/unlisted/public, defaults to draft", type=str, choices=["public", "unlisted", "draft"])

	# read arguments
	args = parser.parse_args()
	print(f'{ args= }')

	data = MediumPublisher.prep_data(vars(args))
	print(f'{ data["title"], data["publishStatus"]= }')

	post_url = MediumPublisher.post_article(data)
	print(f'{ post_url= }')