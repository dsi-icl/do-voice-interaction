import json

import falcon

import requests

class Resource(object):

    def on_post_chatbot(self,req,resp):
        body = json.loads(req.bounded_stream.read())    
        bot_response = requests.post('http://localhost:5002/webhooks/rest/webhook',json=body)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(bot_response.json())
    
    def on_get_status(self,req,resp):

        resp.status = falcon.HTTP_200
        resp.body = 'Service is running'
    
    def on_get_json(self,req,resp):

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'data':'sampleData'})

