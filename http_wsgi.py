import db


def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return [b'Not Found']


def index_html(environ, start_response, template):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [template]


def redirect_url(environ, start_response, hash_url):
    status = '301 Moved Permanently'
    url = db.select_url_db(hash_url)
    response_headers = [
        ('Content-type', 'text/html'),
        ('Location', '{}'.format(url))
    ]
    start_response(status, response_headers)
    return []