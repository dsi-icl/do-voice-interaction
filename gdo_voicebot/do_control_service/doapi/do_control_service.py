import json

import falcon

import requests

class Resource(object):

    def on_post_chatbot(self,req,resp):
        body = json.loads(req.bounded_stream.read())  
        bot_response = requests.post('http://localhost:5002/webhooks/rest/webhook',json=body)  
        try :
            bot_response.raise_for_status()
            resp.status = falcon.HTTP_200
        except requests.HTTPError as exception:
            bot_response = [{"text":"I encountered this error ''" + str(exception) + "'' in the DO control service. Request status : fail."}]
            resp.status = falcon.HTTP_400
        
        if resp.status == falcon.HTTP_200:
            resp.body = json.dumps(bot_response.json())
        else :
            resp.body = json.dumps(bot_response)

    def on_get_status(self,req,resp):

        resp.status = falcon.HTTP_200
        resp.body = 'Service is running'
    
    def on_get_json(self,req,resp):

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'data':'sampleData'})

