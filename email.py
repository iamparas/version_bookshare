import webapp2
from google.appengine.api import mail

def send_email(user,other_user,email):
    message = mail.EmailMessage(sender="",
                            subject="Match Found")
    message.to = user_email
    message.body = """
    Dear """+user+"""
        We have found a match for you. Please Contact"""+other_user+"""
        His email is"""+ email+"""
    The example.com Team
    """

    message.send()
