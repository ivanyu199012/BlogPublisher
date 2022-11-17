#

from publisher import Publisher


class DevTOPublisher( Publisher ):

	@classmethod
	def prep_req_data_dict(self, args):
		raise NotImplementedError

	@classmethod
	def post_article(self, req_data_dict):
		raise NotImplementedError