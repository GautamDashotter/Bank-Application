from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from app.database import get_db
from app.models import RegisterRequest, LoginRequest, TokenResponse
from app.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    request: RegisterRequest,
    db: Database = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.users.find_one({"email": request.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Store hashed password, never the plain password
    user = {
        "name": request.name,
        "email": request.email,
        "password": hash_password(request.password)
    }

    result = db.users.insert_one(user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: LoginRequest,
    db: Database = Depends(get_db)
):
    # Find user by email
    user = db.users.find_one({"email": request.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT
    access_token = create_access_token(
        {
            "sub": str(user["_id"]),
            "email": user["email"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }