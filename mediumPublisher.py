
from publisher import Publisher


class MediumPublisher(Publisher):

	@classmethod
	def format_markdown_text( self, markdown_content : str, id_2_gist_link_dict : dict = None  ) -> str:
		for id, gist_link in id_2_gist_link_dict.items():
			markdown_content = markdown_content.replace( id, gist_link )
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
		raise NotImplementedError