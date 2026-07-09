from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import grpc
import product_pb2
import product_pb2_grpc
from db import get_session
from models import User, UserPublic
from auth import hash_password, verify_password, create_access_token
from shared.jwt_utils import verify_token

router = APIRouter(prefix="/users")


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "user-service"}

@router.post("/login")
def login(user_data: User, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    db_user = session.exec(statement).first()

    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(data={"sub": str(db_user.id), "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserPublic)
def create_user(user: User, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email is already registered."
        )

    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/all", response_model=List[UserPublic])
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}/purchases/{product_id}")
def get_user_purchase(
    user_id: int,
    product_id: int,
    token_data: dict = Depends(verify_token)
):
    if str(user_id) != token_data.get("sub"):
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")

    with grpc.insecure_channel("product-service:50051") as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        response = stub.GetProduct(product_pb2.ProductRequest(id=product_id))

    return {
        "user_id": user_id,
        "product_details": {
            "id": response.id,
            "name": response.name,
            "price": response.price
        },
        "source": "gRPC"
    }


