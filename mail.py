import requests
from flask_mail import Mail

mail = Mail()

def subscribe_user(email, user_group_email, api_key):

    r = requests.post(f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
                         auth=("api", api_key),
                         data={"subscribed": True,
                               "address": email}
                         )
    return r