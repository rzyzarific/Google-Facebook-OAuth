from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
from python_dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = 'abcd'

# URL does not accept 127.0.0.1
app.config['SERVER_NAME'] = 'localhost:5000'

# Initialize OAuth
oauth = OAuth(app)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google/')
def google():
    # Google OAuth Config
    # Get client_id and client_secret from Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get('Google_Client_id')
    GOOGLE_CLIENT_SECRET = os.environ.get('Google_Secret_Key')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print("Google User: ", user)
    return redirect('/')


@app.route('/facebook/')
def facebook():
    # Get client_id and client_secret from Facebook OAuth
    FACEBOOK_CLIENT_ID = os.environ.get('Facebook_Client_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('Facebook_SECRET_KEY')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User: ", profile)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
