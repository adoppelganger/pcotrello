from __future__ import with_statement, print_function, absolute_import
from requests_oauthlib import OAuth1Session

from secret import trello_api_key, trello_api_secret, \
    trello_access_token, trello_access_secret


def create_oauth_token():
    """
    Script to obtain an OAuth token from Trello.
    """
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'

    expiration = 'never'
    scope = 'read,write'
    name = 'PCOTrello'

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and sign the request to obtain
    # said access token.

    session = OAuth1Session(client_key=trello_api_key,
                            client_secret=trello_api_secret)
    response = session.fetch_request_token(request_token_url)
    resource_owner_key = response.get('oauth_token')
    resource_owner_secret = response.get('oauth_token_secret')

    # Step 2: Redirect to the provider. Since this is a CLI script we do not
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print('Go to the following link in your browser:')
    print(f'{authorize_url}?oauth_token={resource_owner_key}'
          f'&scope={scope}&expiration={expiration}&name={name}')

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.

    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me? (y/n) ')
    oauth_verifier = input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this
    # access token somewhere safe, like a database, for future use.
    session = OAuth1Session(client_key=trello_api_key,
                            client_secret=trello_api_secret,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret,
                            verifier=oauth_verifier)
    access_token = session.fetch_access_token(access_token_url)
    print(f'Access token {access_token}')

if __name__ == '__main__':
    create_oauth_token()
