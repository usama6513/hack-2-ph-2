# JWT Authentication Middleware for Better Auth Integration

## Overview
This skill provides a complete implementation of JWT authentication middleware in FastAPI that verifies tokens issued by Better Auth frontend library using a shared secret. It includes setup, middleware implementation, user dependency extraction, and security best practices.

## Prerequisites
- Python 3.9+
- FastAPI
- python-jose[cryptography] for JWT operations
- passlib[bcrypt] for password hashing
- Better Auth configured on the frontend

## Installation

### Required packages:
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-dotenv
```

## Configuration

### Environment Variables (.env):
```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Better Auth Integration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_JWT_SECRET=your-better-auth-jwt-secret
```

### Configuration File (src/core/config.py):
```python
from pydantic_settings import Settings
from typing import Optional


class Settings(Settings):
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Better Auth Configuration
    BETTER_AUTH_JWT_SECRET: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

## JWT Utilities (src/utils/jwt.py):
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from .config import settings


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token issued by Better Auth and return the payload if valid.
    """
    try:
        # Decode the token using the Better Auth JWT secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user information from the payload
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: No user ID found"
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: Signature verification failed"
        )
    except Exception as e:
        print(f"Token verification error: {str(e)}")  # For debugging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token (for cases where you need to issue tokens from backend).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
```

## User Model (src/models/user.py):
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    User model representing the authenticated user extracted from JWT token.
    """
    id: str
    email: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    is_active: bool = True


class TokenData(BaseModel):
    """
    Token data model to represent decoded JWT information.
    """
    user_id: str
    email: str
    expires_at: Optional[datetime] = None
```

## Authentication Middleware & Dependencies (src/core/security.py):
```python
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt import verify_token
from ..models.user import User, TokenData


# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get the current authenticated user from the JWT token in the Authorization header.
    This function verifies the token issued by Better Auth using the shared secret.

    Args:
        credentials: HTTP authorization credentials from the request header

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Verify token and get payload
    payload = verify_token(token)

    # Extract user info from payload
    user_id: str = payload.get("sub")
    email: str = payload.get("email")
    name: str = payload.get("name")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Create and return User object
    token_data = TokenData(user_id=user_id, email=email)

    user = User(
        id=token_data.user_id,
        email=token_data.email,
        name=name
    )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user (additional check for user activation).
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
```

## Example Protected Route (src/api/protected.py):
```python
from fastapi import APIRouter, Depends
from ..models.user import User
from ..core.security import get_current_active_user


router = APIRouter()


@router.get("/protected")
async def read_protected_data(current_user: User = Depends(get_current_active_user)):
    """
    Example of a protected route that requires authentication.
    """
    return {
        "message": "This is protected data",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name
        }
    }


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    """
    return current_user
```

## Main Application Setup (src/main.py):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.protected import router as protected_router
from .core.config import settings


app = FastAPI(title="FastAPI with Better Auth Integration")

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to allow access to token info
    expose_headers=["Access-Control-Expose-Headers", "Authorization"]
)

# Include protected routes
app.include_router(protected_router, prefix="/api/v1", tags=["protected"])

@app.get("/")
def read_root():
    return {"message": "FastAPI with Better Auth JWT Middleware"}
```

## Frontend Integration Notes

### Better Auth Configuration (Frontend):
Ensure your Better Auth configuration includes proper JWT settings:

```javascript
// frontend auth configuration
import { BetterAuth } from "better-auth";

export const auth = BetterAuth({
  // ... other config
  jwt: {
    secret: process.env.BETTER_AUTH_JWT_SECRET, // Same secret used in your FastAPI app
    expiresIn: "30m"
  }
});
```

### API Requests from Frontend:
```javascript
// Example of making authenticated requests to your FastAPI backend
const makeAuthenticatedRequest = async (url, options = {}) => {
  const token = localStorage.getItem('better-auth-session-token');

  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,  // Set header as expected by FastAPI middleware
    }
  });

  if (response.status === 401) {
    // Handle unauthorized access (e.g., redirect to login)
    window.location.href = '/login';
  }

  return response;
};
```

## Best Practices & Security Considerations

### 1. Secret Management
- Store secrets in environment variables, never in code
- Use different secrets for development and production
- Rotate secrets periodically

### 2. Token Validation
- Always verify JWT signature using the shared secret
- Check token expiration
- Validate required claims (user ID, email, etc.)

### 3. Error Handling
- Don't reveal sensitive information in error messages
- Log security-related events internally
- Use consistent error responses for unauthorized access

### 4. CORS Configuration
- Configure CORS properly for production
- Only allow trusted origins
- Consider using environment-specific configurations

### 5. Additional Security
- Use HTTPS in production
- Consider implementing rate limiting for auth endpoints
- Implement proper logging for security events
- Regularly update dependencies

## Testing the Implementation

### Unit Test Example:
```python
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from src.core.config import settings
from src.main import app


def test_protected_route_valid_token():
    client = TestClient(app)

    # Create a test token (in real app, this would come from Better Auth)
    token_data = {"sub": "test_user_123", "email": "test@example.com"}
    test_token = jwt.encode(
        token_data,
        settings.BETTER_AUTH_JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    response = client.get(
        "/api/v1/protected",
        headers={"Authorization": f"Bearer {test_token}"}
    )

    assert response.status_code == 200
    assert "user" in response.json()


def test_protected_route_invalid_token():
    client = TestClient(app)

    response = client.get(
        "/api/v1/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
```

This implementation provides a secure and efficient way to integrate Better Auth JWT tokens with your FastAPI backend, ensuring proper authentication and user identification across your full-stack application.