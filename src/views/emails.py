from flask import Blueprint
from models import User
from utils import create_email_verification_token
from .base import BaseView

bp = Blueprint('user_emails', __name__)

class UserEmailView(BaseView):

    def put(self, user_id):
        user = User.objects.get_or_404(pk=user_id)
        email = self.get_param('email')

        #check for valid email format

        #create email_verification token
        token = create_email_verification_token(client, user, email)

        #use sendgrid to send email verification
        

user_email_view = UserEmailView.as_view('UserEmailView')
bp.add_url_rule('/users/<str: user_id>/emails', view_func=user_email_view, methods=['PUT'])