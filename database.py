from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(50), nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)
    original_plan = Column(Text, nullable=False, default="")
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

def save_user(user_id, username, age, weight, goal, intensity):
    db = SessionLocal()
    try:
        user = User(user_id=user_id, username=username, age=age, weight=str(weight), goal=goal, intensity=intensity)
        db.add(user); db.commit(); db.refresh(user); return user
    finally: db.close()

def save_plan(user_id, plan, nutrition_tip):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.original_plan = plan; user.nutrition_tip = nutrition_tip; db.commit(); db.refresh(user)
        return user
    finally: db.close()

def update_plan(user_id, updated_plan):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.updated_plan = updated_plan; db.commit(); db.refresh(user)
        return user
    finally: db.close()

def get_user(user_id):
    db = SessionLocal()
    try: return db.query(User).filter(User.user_id == user_id).first()
    finally: db.close()

def get_original_plan(user_id):
    user = get_user(user_id); return user.original_plan if user else None

def get_all_users():
    db = SessionLocal()
    try: return db.query(User).order_by(User.id.desc()).all()
    finally: db.close()

def delete_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user: db.delete(user); db.commit(); return True
        return False
    finally: db.close()
