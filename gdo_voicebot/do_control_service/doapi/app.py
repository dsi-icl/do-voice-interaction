import falcon

from .do_control_service import Resource

api = application = falcon.API()

do_control_api = Resource()

api.add_route('/api/status',do_control_api,suffix='status')
api.add_route('/api/json',do_control_api,suffix='json')
api.add_route('/api/chatbot',do_control_api,suffix='chatbot')