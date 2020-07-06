import falcon
import os

class ExampleClass(object):
    def __init__(self):
        self.full_path = 'C:\\Users\\Matt Congreve\\AppData\\Local\\Temp\\example.txt'

    def on_post(self, req, resp):
        req_media = req.media
        if 'content' in req_media:
            content = req_media['content']
            try:
                with open(self.full_path, 'w') as fd:
                    fd.write(content)
                resp.media = {'ok': True}
            except Exception as ex:
                resp.media = {'ok': False, 'exception': repr(ex)}
                resp.status = falcon.HTTP_500
        else:
            resp.media = {'ok': False}
            resp.status = falcon.HTTP_422

    def on_get(self, req, resp):
        try:
            with open(self.full_path, 'r') as fd:
                content = fd.read()
            resp.media = {'ok': True, 'content': content}
        except Exception as ex:
            resp.media = {'ok': False, 'content': None, 'exception': repr(ex)}
            resp.status = falcon.HTTP_500




example_class = ExampleClass()

app = falcon.API()

app.add_route('/example', example_class)