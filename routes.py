from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import revise_plan
from .database import save_user, save_plan, update_plan, get_user, get_original_plan, get_all_users, delete_user, SessionLocal
from .database import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request, username: str=Form(...), user_id: str=Form(...), age: int=Form(...), weight: float=Form(...), goal: str=Form(...), intensity: str=Form(...)):
    if not 13 <= age <= 100: raise HTTPException(400, "Age must be between 13 and 100.")
    if weight <= 0: raise HTTPException(400, "Weight must be greater than zero.")
    plan = generate_workout_gemini(age, weight, goal, intensity)
    tip = generate_nutrition_tip_with_flash(goal)
    existing = get_user(user_id)
    if existing:
        db = SessionLocal()
        try:
            existing.username, existing.age, existing.weight = username, age, str(weight)
            existing.goal, existing.intensity = goal, intensity
            existing.original_plan, existing.updated_plan, existing.nutrition_tip = plan, None, tip
            db.commit()
        finally: db.close()
    else:
        save_user(user_id, username, age, weight, goal, intensity); save_plan(user_id, plan, tip)
    return templates.TemplateResponse("result.html", {"request":request,"username":username,"user_id":user_id,"age":age,"weight":weight,"goal":goal,"intensity":intensity,"workout_plan":plan,"nutrition_tip":tip,"updated":False})

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str=Form(...), feedback: str=Form(...)):
    user = get_user(user_id)
    if not user: raise HTTPException(404, "User ID not found.")
    updated = revise_plan(get_original_plan(user_id), feedback, user.goal, user.intensity)
    update_plan(user_id, updated)
    return templates.TemplateResponse("result.html", {"request":request,"username":user.username,"user_id":user.user_id,"age":user.age,"weight":user.weight,"goal":user.goal,"intensity":user.intensity,"workout_plan":updated,"nutrition_tip":user.nutrition_tip,"updated":True})

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    return templates.TemplateResponse("all_users.html", {"request":request,"users":get_all_users()})

@router.post("/delete-user/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id); return RedirectResponse("/view-all-users", status_code=303)
