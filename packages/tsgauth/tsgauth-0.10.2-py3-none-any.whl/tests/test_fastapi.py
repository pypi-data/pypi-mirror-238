from fastapi import FastAPI,Depends
from fastapi.testclient import TestClient
from tsgauth.fastapi import JWTBearerClaims
import tsgauth

### test server setup
app = FastAPI()
client = TestClient(app)
client_id = "cms-tsg-frontend-testclient"
client_id_wrong = "not_a_real_client"
auth = tsgauth.oidcauth.KerbAuth(client_id)

@app.get("/unsecure")
async def unsecure():
    return {"msg": "unsecure endpoint"}

@app.get("/secure")
async def secure(claims = Depends(JWTBearerClaims(client_id=client_id))):
    return {"msg": f"welcome {claims['sub']}"}

@app.get("/secure_wrong_aud")
async def secure(claims = Depends(JWTBearerClaims(client_id=client_id_wrong))): 
    return {"msg": f"welcome {claims['sub']}"}


### tests
def test_unsecure():
    """
    simple test to just check we started the fastapi server correctly
    """    
    resp = client.get('/unsecure')
    assert resp.status_code == 200
    assert resp.json()['msg'] == 'unsecure endpoint'

def test_secure_noauth():
    """
    test that we fail the auth when we dont pass in the correct authentication parameters
    """    
    resp = client.get('/secure')
    assert resp.status_code == 401

def test_secure_auth():
    """
    test that we can authenticate and get the username back
    """
    resp = client.get('/secure',**auth.authparams())
    subject = tsgauth.oidcauth.parse_token(auth.token())["sub"]
    assert resp.status_code == 200
    assert resp.json()['msg'] == f'welcome {subject}'

def test_secure_wrong_aud():
    """
    test that we reject tokens with the wrong auth
    """
    resp = client.get('/secure_wrong_aud',**auth.authparams())
    assert resp.status_code == 403
    assert resp.json()['detail'] == f'Invalid token audience, expects {client_id_wrong}'
