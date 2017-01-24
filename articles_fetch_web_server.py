from flask import Flask
from urllib2 import Request, urlopen, URLError
from article_fetch import fetch_pocket_links
import json

app = Flask(__name__)


@app.route('/fetch_cached')
def fetch_cached():
    return open('articles.json', 'r').read()


@app.route('/fetch/<user_id>')
def fetch(user_id):
    request = Request('http://pocket_square_users:28101/user/' + user_id)

    try:
        response_json = urlopen(request).read()
        response = json.loads(response_json)
        return json.dumps(fetch_pocket_links(response.accessToken))
    except URLError, e:
        if hasattr(e, 'reason'):
            return 'Something went wrong:', e.reason
        if hasattr(e, 'code'):
            return 'Something went wrong:', e.code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
