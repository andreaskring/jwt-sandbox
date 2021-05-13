# Usage: provide access token as first command line argument, e.g.
# $ python sandbox.py <token>

import sys
import jwt


JWKS_URI = 'http://localhost:8080/auth/realms/demo/protocol' \
           '/openid-connect/certs'

access_token = sys.argv[1]
client = jwt.PyJWKClient(JWKS_URI)

signing = client.get_signing_key_from_jwt(access_token)

data = jwt.decode(
    access_token,
    signing.key,
    algorithms=['RS256']
)
