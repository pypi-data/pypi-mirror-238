# tsgauth

A collection of python base CERN SSO based authentication and authorisation tools used by the TSG. It provides methods for both users trying to access SSO protected sites in python and for sites to add SSO protection to their endpoints. It is minimal and tries to stay out of the way of the user as much as possible.

The current version is 0.10.2

It is pip installable by 
```bash
pip3 install tsgauth==0.10.2
pip3 install tsgauth[flask]==0.10.2  #if you want flask modules
pip3 install tsgauth[fastapi]==0.10.2 #if you want fastapi modules
```

Version policy: The major version number will be incremented for any breaking changes. The minor version number will be incremented for any new features. The patch version number will be incremented for any bug fixes. The package is currently in development and will be so till it hits version 1.0.0, until then these rules will be a bit looser.

It is intended that users use keyword arguments when passing into the function as the order of the arguements may change in minor versions with the exception of client_id which is always first. Only public methods and members (ie do not start with _) are considered part of the API and thus subject to the version policy. Changes to the internals will not be considered breaking changes but will be considered enough to bump the minor version number.

Support requests can be raised on the [gitlab issue tracker](https://gitlab.cern.ch/cms-tsg-fog/tsgauth/-/issues) or by contacting Sam Harper on mattermost (prefered)

## Security Warning

To use this package securely there are two things you need to do:

1. if you use the option to persist sessions ensure that the resulting authentication files stored in ~/.tsgauth are not compromised. Whoever has these files has the privileges they represent. They are created to be only read/writable by the user but if you copy them about, you need to ensure they are protected.
1. if you use pip, **always specify a version**, ie `pip3 install tsgauth==0.10.1` not `pip3 install tsgauth` to prevent a [supply chain attack](https://en.wikipedia.org/wiki/Supply_chain_attack). This is a good idea for packages in general but is critical here. Otherwise you are trusting that a malicious actor has not compromised my pypi account and uploaded a malicious version of the package which could either intercept OTPs or send the resulting authentication files to a remote server. It would not be possible for them to access your password, just the auth session cookie/ access token. Note, it is not possible for anybody to upload new code as an existing version to pypi, ie `pip3 install tsgauth==0.10.1` will always install the same code.


## Quick start

### How to Access SSO CERN sites in python using TSGAuth

This is a minimal explaination for the impatient who just want to access a SSO protected website using python. For a more detailed explaination, please see the rest of this guide. TSGAuth is designed assuming you are using the `requests` module but exposes methods which will work with any module which can make http requests assuming you can pass cookies and headers to it.


There are different ways to access SSO protected sites on the cmdline, there are a series of classes in tsgauth.oidcauth for various types of authorsization and authentication mechanisms. They are all designed such that

```python
auth = tsgauth.oidcauth.<AUTHCLASS>()
r = requests.get(url,**auth.authparams()) #note depending on the auth class, it may override your headers, thus you need to 
                                          #pass in any headers you want in the authparams call, eg
                                          #**auth.authparams(headers={"Accept":"application/json"})
```
will work for all of them.

The only thing the user needs to do is select the correct class. To do this you need to know if the website (aka protected resource) you which to access is using session/cookie or token based authorisation. 

If its cookie based, you will need to use a SessionAuth derived class of which the only one is `tsgauth.oidcauth.KerbSessionAuth()` which uses kerberos to authenticate. If it is token based, you need a TokenAuth class, of which there are three, `tsgauth.oidcauth.KerbAuth()`, `tsgauth.oidcauth.ClientAuth()` and `tsgauth.oidcauth.DeviceAuth()` depending on how you wish to authenticate.  You will also need to know the client id of the application you wish to access as well as its redirect_uri. If it is a confidential client, you will also need the client secret.

Most users will want `tsgauth.oidcauth.KerbAuth()` which uses kerberos to authenticate. Unlike the CERN sso-get-cookie and sso-get-token, tsgauth supports accounts with 2FA enabled (the author of this package has 2FA enabled...)

examples using kerberos 

```python
auth = tsgauth.oidcauth.KerbAuth("cms-tsg-frontend-client")
r = requests.get("https://hltsupervisor.app.cern.ch/api/v0/thresholds",**auth.authparams())
```

```python
auth = tsgauth.oidcauth.KerbSessionAuth()
r = requests.get("https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies?raw=text",**auth.authparams())
```

As a final heads up, the AuthClasses can persist cookies and tokens to disk so you dont need to reauthenticate every time. This is true by default for KerbSessionAuth, DeviceAuth classes. The directory should only be readable by the user and is `~/.tsgauth` by default but you can override it by setting the `TSGAUTH_AUTHDIR` environmental variable.  **These files should be protected as they grant access as you to the given application.** Note, it is not an error for the application to fail to read/write to this directory, it will continue as is but log a warning. The logging level is controled by the `TSGAUTH_LOGLEVEL` environmental variable and defaults to `ERROR`. The writing of the authentication files is controled by the parameter `use_auth_file` passed in the constructor of the auth class. For convenience you can also force enabling / disabling of this feature globally by setting the environmental variables `TSGAUTH_FORCE_USE_AUTHFILE` / `TSGAUTH_FORCE_DONT_USE_AUTHFILE` to 1. 

A summary of the enviromental variables is as follows:
 * TSGAUTH_LOGLEVEL : logging level ("NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
 * TSGAUTH_AUTHDIR : directory where the auth files are written if requested to be (default: ~/.tsgauth)) 
 * TSGAUTH_FORCE_USE_AUTHFILE : forces the authfile to be written/used (set to 1 to do this)
 * TSGAUTH_FORCE_DONT_USE_AUTHFILE : forces the authfile to not be written/used  (set to 1 do this)

#### Determing if a resource expects Session or Cookie based authorisation

The easiest way to find out how to service expects you to authenticate is ask the owner or review their documenation. As this is not always possible, you can open it up in a webbrowser and see how the browser is making requests. 

If you see the the requests to the protected api  have a header {"Authorization", "Bearer <long string>}" it is token based. You should also see the browser requesting said token, with something like:

```
https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/auth?client_id=cms-tsg-frontend-client&redirect_uri=https%3A%2F%2Fhltsupervisor.app.cern.ch%2F&state=8dbacbe6-e06e-4fb9-8699-eb87c136195a&response_mode=fragment&response_type=code&scope=openid&nonce=3d5ff976-fd51-43aa-8b0d-3a72c2782b20
```
this gives your client_id (cms-tsg-frontend-client) and a valid redirect_uri (https://hltsupervisor.app.cern.ch/) which you can use to request a token.

If you dont see anything like this, its session based (you'll probably see a cookie auth session or similar). Session Cookie auth is mainly done public services using confidential clients. The client (say an apache server which is interacting with the resource server on your behalf) handles the token exchange and the user never sees the token. It will instead issue you a cookie so identify you for the authentication session. 

### Securing FastAPI sites

If you wish to secure an endpoint on your fast api system, you just need to make your endpoint depend on tsgauth.fastapi.JWTBearerClaims. This will validate the user claims (unless validate_token=False) and make them available to your endpoint. Note: I've only recently started using fastapi so while I think this is a good way to do it, there may be better ways which more experienced fastapi users can suggest.

```python
from tsgauth.fastapi import 
@app.get("/api/v0/secure")
def secure_endpoint(claims = Depends(JWTBearerClaims("your-client-id"))):
   return {"claims" : claims}
```
This will validate the user claims with an audience of your_client_id and make the claims available to your endpoint. If you have no further need of the the claims info, you can put the depends in the decorator. 

You can see an example of this in the tests/test_fastapi.py file which is run as part of the unit tests

### Securing Flask sites

In python this was modeled after the flask-oidc package which is completely not recommended but when we started we ended up using due to very inadequate documenation. It requires the following variables to be set in your flask configuration

```python
app.config.update({
   'OIDC_ISSUER' : "https://auth.cern.ch/auth/realms/cern"
   'OIDC_JWKS_URI' : "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect/certs"
   'OIDC_CLIENT_ID' : <your client id>   
}) 
```

and then can be used as follows

```python
import tsgauth.flaskoidc as oidc
@application.route('/api/v0/secure', methods=['GET'])
@oidc.accept_token(require_token=True)
def secure_endpoint():
      return jsonify({"claims" : g.oidc_token_info})
```

You can see an example of this in the tests/test_flaskoidc.py file which is run as part of the unit tests