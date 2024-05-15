from model.user import Users, UserCreate
from sqlalchemy.orm import Session
from controllers.password_hasheado import hash_password, verify_password

def authenticate_user(full_name: str, password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    db_user = Users(full_name=user.full_name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(full_name: str, db: Session):
    return db.query(Users).filter(Users.full_name == full_name).first()

def delete_user(full_name: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def change_password(full_name: str, new_password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        user.password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return True
    return False
