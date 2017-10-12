from wsgiref.simple_server import make_server
from spichi import create_app
from views import View
from session import session
from utils import redirect
from autoreload import autoreload


app = create_app()
cache = app.caches['redis'].cache

@app.route('/', 'home')
def home(request):
    return 'home'


@app.route_class('/hello', 'hello')
class Hello(View):
    def get(self, request):
        if session['count'] != None:
            session['count'] += 1
        else:
            session['count'] = 0
        print session['count']
        session.save()
        return redirect('/')

    def post(self, request):
        return 'post hello'


def run():
    httpd = make_server(host='', port=8848, app=app)
    # a method of BaseServer, which's in /lib/python2.7/SocketServer.py
    httpd.serve_forever()


if __name__ == '__main__':
    autoreload(run)
