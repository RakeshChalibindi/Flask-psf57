# email templates
class EmailTemplates:
    def OTPEmailTemplate(username:str, otp:int):
        return f"""Hello {username},
        Thanks for registering to SNS - Management app
        your OTP:{otp}

        If you are not register for app ignore this email and don't OTP with any one.
        Regards
        SNS-Management app
        """