# Usage: provide access token as first command line argument, e.g.
# $ python sandbox.py <token>

from pprint import pprint
import sys
import jwt
import cryptography.hazmat.primitives.serialization


JWKS_URI = 'http://localhost:8081/auth/realms/mo/protocol' \
           '/openid-connect/certs'

access_token = sys.argv[1]
client = jwt.PyJWKClient(JWKS_URI)

signing = client.get_signing_key_from_jwt(access_token)

data = jwt.decode(
    access_token,
    signing.key,
    algorithms=['RS256']
)
pprint(data)

# Encoding with own key

# Create key pair with
# ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
# openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
# (see https://gist.github.com/ygotthilf/baa58da5c3dd1f69fae9)

with open('jwtRS256.key', 'rb') as fp:
    pri = fp.read()

with open('jwtRS256.key.pub', 'rb') as fp:
    pub = fp.read()

token = jwt.encode({'some': 'payload'}, pri, algorithm='RS256')
payload = jwt.decode(token, pub, algorithms='RS256')

# Read key from file to object

with open('jwtRS256.key', 'rb') as fp:
    key = cryptography.hazmat.primitives.serialization.load_pem_private_key(
        fp.read(),
        password=None
    )

