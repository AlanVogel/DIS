from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    """Create a JWT access token with an expiration time.

    Encodes the input data into a JWT token with a 30-minute expiration.

    Args:
        data (dict): Data to encode in the token (e.g., user info).

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Verify a JWT token and return its payload.

    Decodes and validates the token using the secret key.

    Args:
        token (str): JWT token to verify.

    Returns:
        dict: Decoded token payload.

    Raises:
        HTTPException: If token verification fails (401).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
