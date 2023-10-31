import tsgauth.oidcauth
import authlib

try:
    from fastapi import HTTPException, status, Request
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
except ImportError:
    HTTPException = status = Request = None
    class HTTPBearer:
        pass
    HTTPAuthorizationCredentials = None

"""
collection of functions for use with fastapi
note: this is the authors first time using fastapi, so there may be better ways to do this.
      this package will evolve in the future as experience is gained
"""


def _check_fastapi():
    if Request is None:
        raise ImportError(
            "fastapi is not installed, to you use this object you must install fastapi\n"
            "pip install fastapi or "
            "pip install tsgauth[fastapi]"
        )

class JWTBearerClaims(HTTPBearer):
    def __init__(self, client_id :str, validate_token :bool = True, auto_error: bool = False):
        """
        gets the decoded claims from the request header
        :param client_id: the client id required for the audience claim
        :param validate_token: whether or not to validate the token, if false it'll just return the claims
        :auto_error: this is for the base class BearerAuth, if true it'll raise an exception if the token is not present
                     I would use this but it returns a 403 code rather than a 401 in this case which is incorrect :(
        """
        _check_fastapi()
        super(JWTBearerClaims, self).__init__(auto_error=auto_error)
        self.client_id = client_id
        self.validate_token = validate_token

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerClaims, self).__call__(request)        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            print("credentials",credentials)
            try:
                claims = tsgauth.oidcauth.parse_token(credentials.credentials, 
                                                      client_id = self.client_id, 
                                                      validate=self.validate_token)  
                return claims
            except authlib.jose.errors.InvalidClaimError as e:
                if e.description == 'Invalid claim "aud"':
                    raise HTTPException(status_code=403, detail=f"Invalid token audience, expects {self.client_id}")
                else:
                    raise HTTPException(status_code=403, detail="Invalid token")
            except Exception as e:            
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
        else:
            #only gets called if auto_error is false, otherwise the base class will raise the exception
            raise HTTPException(status_code=401, detail="No authentication credentials provided.")

        