from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    """Login request payload."""
    username: str = Field(..., description="User account name")
    password: str = Field(..., description="User password (plain text over HTTPS)")

# PUBLIC_INTERFACE
class AuthToken(BaseModel):
    """Bearer JWT token response."""
    token: str = Field(..., description="JWT bearer token")
