# StreamlitGAuth

StreamlitGAuth is a Python library that simplifies the integration of Google Authenticator-based Single Sign-On (SSO) with Streamlit applications. With StreamlitGAuth, you can enhance the security of your Streamlit apps by enabling two-factor authentication through Google Authenticator.

![Sample image](https://github.com/Rahulkatoch99/Appening-assigment/blob/master/streamlitGauth.png?raw=true)

## Installation

You can install StreamlitGAuth using pip

# Usage

```python
from google_auth.google_auth import GoogleAuth
import streamlit

client_id = "your_client_id"
client_secret = "your_client_secret"
login = GoogleAuth(client_id, client_secret)

if login:
    print("Login successful")


```

Replace "your_client_id" and "your_client_secret" with your actual Google OAuth 2.0 credentials.

# Example Streamlit Application

```python

import streamlit as st
from google_auth import Google_auth


client_id = "hasjh5jk498ufiu3h89g8-aghdszjhk3k.apps.googleusercontent.com"
client_secret = "afsghfbkhfdjdsgfdjhfjkfhjkfhkjhkjdhks"

login = Google_auth(clientId=client_id, clientSecret=client_secret)

if login == "authenticated":
    # your streamlit applciation
    pass

else:
    st.warning("login failed")

```

# Contributing

If you would like to contribute to StreamlitGAuth, please open an issue or submit a pull request on our GitHub repository.

# License

This library is released under the [MIT License](LICENSE) to encourage collaboration and use in various applications.
