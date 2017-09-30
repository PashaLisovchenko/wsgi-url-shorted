from urllib.parse import parse_qs
from html import escape
import db
import http_wsgi as hw
import os
from string import Template
from hashlib import md5

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def render(template_name):
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    mass_hash = db.select_hash_db()
    with open(template_path, 'r') as f:
        response_body = f.read()
        response_body += '<p>hash in data base</p><ul>'
        for h in mass_hash:
            response_body += h
        response_body += '</ul>'
    template = Template(response_body).safe_substitute().encode()
    return template


def take_hash(url):
    url_hash = md5(url.encode('utf-8')).hexdigest()
    return url_hash[:8]


def take_url_post(environ):
    try:
        size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        size = 0
    data = environ['wsgi.input'].read(size)
    m_data = parse_qs(data.decode())
    url = m_data['url'][0]
    url_hash = take_hash(url)
    db.add_db_url(url_hash, url)
    print('{} - {}'.format(url_hash, url))


def app(environ, start_response):
    template = render('index.html')
    if environ['REQUEST_METHOD'] == 'POST':
        take_url_post(environ)
    elif environ['REQUEST_METHOD'] == 'GET':
        path_inf = environ.get('PATH_INFO', '')
        path = path_inf.split('/')
        qs = parse_qs(environ['QUERY_STRING'])
        if path[1] != '':
            try:
                return hw.redirect_url(environ, start_response, path[1])
            except TypeError:
                return hw.not_found(environ, start_response)
        elif len(qs) > 0:
            try:
                url_hash = escape(qs.get('hash', [''])[0])
                return hw.redirect_url(environ, start_response, url_hash)
            except TypeError:
                return hw.not_found(environ, start_response)
    return hw.index_html(environ, start_response, template)


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        http_srv = make_server('localhost', 8080, app)
        http_srv.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
