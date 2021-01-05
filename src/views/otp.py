from random import randint

from .base import BaseView


class OTPView(BaseView):

    def post(self):
        identifier_type = self.get_param()