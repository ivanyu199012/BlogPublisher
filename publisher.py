#

class Publisher:

	@classmethod
	def prep_req_data_dict(self, args, markdown_content) -> dict:
		raise NotImplementedError

	@classmethod
	def post_article(self, req_data_dict) -> str:
		raise NotImplementedError