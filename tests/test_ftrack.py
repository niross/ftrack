from tests.base import BaseTest


class FTrackTest(BaseTest):
    def test_homepage_unauthenticated(self):
        response = self.client.get('/')
        assert response.status_code == 302
