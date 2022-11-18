
from publisher import Publisher


class MediumPublisher(Publisher):

	@classmethod
	def format_markdown_text( self, markdown_content : str, id_2_gist_link_dict : dict = None  ) -> str:
		return markdown_content.replace( "# ", "## " )

	@classmethod
	def prep_req_data_dict(self, args, markdown_content) -> dict:
		raise NotImplementedError

	@classmethod
	def post_article(self, req_data_dict) -> str:
		raise NotImplementedError