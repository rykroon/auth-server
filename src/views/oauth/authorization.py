from urllib.parse import quote, urlencode
from flask import jsonify, redirect, request
from flask.views import MethodView
from models import Client
from tokens import create_authorization_code


class Authorize(MethodView):
    def get(self):
        self.validate_request()

        query_args = {
            'code': create_authorization_code(
                self.code_challenge, 
                self.code_challenge_method
            ),
        }

        if self.state:
            query_args['state'] = self.state

        location = "{}?{}".format(
            self.redirect_uri, 
            urlencode(query_args, quote_via=quote)
        )

        """
            The authorization server validates the request to ensure that all
            required parameters are present and valid.  If the request is valid,
            the authorization server authenticates the resource owner and obtains
            an authorization decision (by asking the resource owner or by
            establishing approval via other means).
        """
        return redirect(location=location)

    def validate_request(self):
        self.response_type = request.args.get('response_type')
        if self.response_type != 'code':
            raise Exception

        self.client_id = request.args.get('client_id')
        client = Client.objects.get(uuid=self.client_id)
        if client is None:
            raise Exception

        self.code_challenge = request.args.get('code_challenge')
        if self.code_challenge is None:
            raise Exception

        self.code_challenge_method = request.args.get('code_challenge_method', 'plain')
        if self.code_challenge_method not in ('S256', 'plain'):
            raise Exception

        self.redirect_uri = request.args.get('redirect_uri')
        if self.redirect_uri and self.redirect_uri not in client.redirect_uri:
            raise Exception

        self.scope = request.args.get('scope')
        self.state = request.args.get('state')