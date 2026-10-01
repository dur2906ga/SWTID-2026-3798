from .gemini_generator import update_workout_plan

def revise_plan(original_plan, feedback, goal, intensity):
    return update_workout_plan(original_plan, feedback, goal, intensity)
