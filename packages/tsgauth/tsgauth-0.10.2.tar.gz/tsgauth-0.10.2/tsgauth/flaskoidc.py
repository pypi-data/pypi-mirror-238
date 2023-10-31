import logging
import functools
from authlib.oidc.core import UserInfo
try:
    from flask import current_app, request, jsonify, g
except ImportError:
    current_app = request = jsonify = g = None    
import tsgauth.oidcauth

"""
inspired by https://gitlab.cern.ch/authzsvc/docs/flask-oidc-api-example
to replace flask-oidc which is old and out of date (https://github.com/puiterwijk/flask-oidc)

Adds basic OpenID Connect authorisation to a flask server


decorate every endpoint you wish to protect with accept_token and the User info (if valid) will be in g.oidc_token_info

TODO: handle the nonce better, but need to see a workflow example first


author Sam Harper (STFC-RAL, 2022)
"""

def _check_flask():
    if request is None:
        raise ImportError("flask is not installed, to you use this function you must install flask\n"
                          "pip install Flask or "
                          "pip install tsgauth[Flask]"
                          )

def _require_flask():
    def decorate(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            _check_flask()
            return func(*args, **kwargs)
        function_wrapper.__name__ = func.__name__
        return function_wrapper
    return decorate


def parse_token(token,jwks_url="https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs",            
                issuer="https://auth.cern.ch/auth/realms/cern",
                client_id=None,validate=True):
    print("WARNING: tsgauth.flaskoidc.parse_token is depreciated, please use tsgauth.oidcauth.parse_token instead")
    return tsgauth.oidcauth.parse_token(token,jwks_url,issuer,client_id,validate)

@_require_flask()
def _parse_token_flask(token,validate):
    """
    parses a token (optionally validated) but retrieving the parameters from the flask app config

    :param token: the token to parse
    :param validate: validate the parsed token
    :returns: the parsed token as an authlib.oidc.core.IDToken
    :rtype: authlib.oidc.core.IDToken
    """
    return tsgauth.oidcauth.parse_token(token = token,
        jwks_url = current_app.config["OIDC_JWKS_URI"],
        issuer = current_app.config["OIDC_ISSUER"],
        client_id = current_app.config["OIDC_CLIENT_ID"],
        validate=validate
    )            
    
@_require_flask()
def accept_token(require_token=True):
    """
    decorator for validation of the auth token

    puts the claims (if validated) into g.odic_token_info

    note UserInfo is just a dict which parses the keys of IDToken, ie its just the claims of the IDToken without the 
    rest of the methods

    :params require_token: if true , a valid token is required, otherwise is optional and method will succeed
    :returns: None
    """
    
    def decorator(func):
        @functools.wraps(func)
        def function_wrapper(*args, **kwargs):
            try:
                auth_header = request.headers["Authorization"]
                token = auth_header.split("Bearer")[1].strip()                
                claims = _parse_token_flask(token,validate=True)
                g.oidc_token_info = UserInfo(claims)                
            except Exception as e:
                g.oidc_token_info = None
                logging.error(f"Authentication error: {e}")
                if require_token == True:
                    return jsonify({"status": "Computer says no"}), 401
            return func(*args, **kwargs)
        function_wrapper.__name__ = func.__name__
        return function_wrapper
    return decorator
