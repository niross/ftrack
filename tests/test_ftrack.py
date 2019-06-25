from urllib.parse import unquote

from flask_security import url_for_security

from tests.base import BaseTest


class FTrackTest(BaseTest):
    def test_homepage_unauthenticated(self):
        with self.client as c:
            response = c.get('/')
            login_url = url_for_security('login', _external=True) + '?next=/'
            assert unquote(response.location) == login_url
