import os
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY: genai.configure(api_key=API_KEY)

def generate_workout_gemini(age, weight, goal, intensity):
    if not API_KEY: return fallback_workout(age, weight, goal, intensity)
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""Create a personalized 7-day fitness workout plan.
Age: {age}; Weight: {weight} kg; Goal: {goal}; Intensity: {intensity}.
For every day include focus, 5-10 minute warm-up, exercises with sets/reps or duration,
rest intervals, and cooldown/recovery. Include appropriate recovery/rest. Keep it practical.
Do not provide diagnosis or medical treatment."""
    return model.generate_content(prompt).text

def update_workout_plan(original_plan, feedback, goal, intensity):
    if not API_KEY:
        return f"UPDATED PLAN\n\nOriginal plan:\n{original_plan}\n\nRequested change:\n{feedback}\n\nGoal: {goal}\nIntensity: {intensity}\n\nPlease apply the requested adjustment while keeping the plan practical."
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""Rewrite the complete 7-day workout plan below using the user's feedback.
Goal: {goal}; Intensity: {intensity}
Original plan:\n{original_plan}
Feedback:\n{feedback}
Return the complete revised plan with warm-up, main workout, sets/reps or duration,
rest, and cooldown/recovery. Do not provide diagnosis or medical treatment."""
    return model.generate_content(prompt).text

def fallback_workout(age, weight, goal, intensity):
    return f"""FITBUDDY 7-DAY WORKOUT PLAN\n\nProfile: Age {age} | Weight {weight} kg | Goal {goal} | Intensity {intensity}\n\nDay 1 - Full Body\nWarm-up: 5-10 min walk and mobility\nMain: Squats 3x10, Push-ups 3x8-12, Rows 3x10, Glute bridges 3x12\nCooldown: 5 min stretching\n\nDay 2 - Cardio & Core\nWarm-up: 5 min easy cardio\nMain: Cardio 20-30 min, Plank 3x30 sec, Dead bug 3x10/side\nCooldown: 5-10 min stretching\n\nDay 3 - Upper Body\nWarm-up: 5-10 min shoulder mobility\nMain: Push-ups 3x8-12, Rows 3x10, Shoulder press 3x10\nCooldown: Upper-body stretching\n\nDay 4 - Recovery\nEasy walking 20-30 min plus gentle mobility.\n\nDay 5 - Lower Body\nWarm-up: 5-10 min\nMain: Squats 3x10, Lunges 3x8/leg, Romanian deadlift 3x10, Calf raises 3x15\nCooldown: Lower-body stretching\n\nDay 6 - Cardio & Core\nWarm-up: 5 min\nMain: Cardio 20-30 min, Side plank 3x20-30 sec/side, Bird dog 3x10/side\nCooldown: 5-10 min\n\nDay 7 - Active Recovery\nEasy walk, light mobility and stretching for 20-30 minutes.\n\nAdjust exercises to your fitness level and stop if an exercise causes pain."""
