from Config.config import settings;
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="api-key")
def validate_auth_key(header_value: str = Security(api_key_header)):
    if not header_value:
        raise HTTPException(status_code=401, detail="Missing Authentication key")
    if settings.KEY != header_value:
        raise HTTPException(status_code=401, detail="invalid Authentication key")
