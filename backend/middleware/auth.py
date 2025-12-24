from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt
import logging

logger = logging.getLogger(__name__)

# Security Schemes
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
security = HTTPBearer(auto_error=False)

# Configuration from Env
MAAS_API_KEY = os.getenv("MAAS_API_KEY_SECRET", "dev-secret-key")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt-secret")
JWT_ALGORITHM = "HS256"

async def get_current_user(
    api_key: str = Security(api_key_header),
    token: HTTPAuthorizationCredentials = Security(security)
):
    """
    Validates authentication via API Key or JWT Token.
    Returns user identity or raises 401.
    """
    # 1. Check API Key
    if api_key:
        if api_key == MAAS_API_KEY:
            return {"user_id": "api-key-user", "role": "admin"}
        # If API key is present but invalid, we might want to return error or try JWT?
        # Let's say if present it must be valid.
    
    # 2. Check JWT
    if token:
        try:
            payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    # If neither provided or valid
    if not api_key and not token:
        raise HTTPException(status_code=401, detail="Missing authentication credentials")
        
    raise HTTPException(status_code=401, detail="Invalid credentials")

def verify_auth(user: dict = Depends(get_current_user)):
    """
    Dependency to enforce auth on routes.
    """
    return user
