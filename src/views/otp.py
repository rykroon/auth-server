from random import randint

from utils import Cache
from .base import BaseView


class OTPView(BaseView):

    def post(self):
        identifier_type = self.get_param('identifier_type', choices=('email', 'phone_number'))
        identifier = self.get_param('identifier')

        otp = str(randint(0, 999999)).zfill(6)

        cache = Cache('one-time-password')
        cache.set(otp, True)


        #reasons 
        # verify email/ phone number
        # sign in with email / phone number
        # 
        #