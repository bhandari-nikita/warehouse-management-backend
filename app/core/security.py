from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "WMB_key"  #server uses this key to create token. Server also uses this key to verify token
ALGORITHM = "HS256"   #→ Algorithm used to digitally sign token. HS256 is a common choice for symmetric signing, where the same secret key is used for both signing and verifying the token.

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
# Function to create JWT access token
def create_access_token(data: dict): #data contains payload information.
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    # creates actual JWT token by encoding the payload (to_encode) with the secret key and algorithm.
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt