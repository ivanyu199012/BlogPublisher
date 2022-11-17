#

from publisher import Publisher


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
			articles_dict['tags'] = [t.strip() for t in args['tags'].split(',')]

		return {
			"article" : articles_dict
		}

	@classmethod
	def post_article(self, req_data_dict) -> str:
		raise NotImplementedError