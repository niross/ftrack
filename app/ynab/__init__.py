import flask
from flask import request, url_for, redirect, current_app
from flask_dance import OAuth2ConsumerBlueprint
from flask_dance.consumer import oauth_before_login


class CustomYnabOauth(OAuth2ConsumerBlueprint):
    """
    We need to override the login method if the app is in debug/testing mode
    as YNAB requires a specific redirect for local hosts and flask-dance
    does not support this.
    """
    ynab_localhost = 'urn:ietf:wg:oauth:2.0:oob'

    def login(self):
        self.session.redirect_uri = url_for(
            ".authorized", next=request.args.get("next"), _external=True
        )
        if current_app.debug or current_app.testing:
            # self.session.redirect_uri = self.ynab_localhost + url_for(".authorized", next=request.args.get("next"))
            self.session.redirect_uri = self.ynab_localhost
        url, state = self.session.authorization_url(
            self.authorization_url, state=self.state, **self.authorization_url_params
        )
        state_key = "{bp.name}_oauth_state".format(bp=self)
        flask.session[state_key] = state
        oauth_before_login.send(self, url=url)
        return redirect(url)


def make_ynab_blueprint(client_id, client_secret):
    return CustomYnabOauth(
        'ynab',
        __name__,
        client_id=client_id,
        client_secret=client_secret,
        base_url='https://app.youneedabudget.com',
        token_url='https://app.youneedabudget.com/oauth/token',
        authorization_url='https://app.youneedabudget.com/oauth/authorize',
    )
