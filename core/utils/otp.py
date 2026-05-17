import random

class Otp:
    @staticmethod
    def generate_random_otp(length=6):
         return str(random.randint(100000, 999999))
        