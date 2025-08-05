from datetime import datetime
from google.adk.agents import Agent

# --- Premium calculation logic ---
def calculate_premium(car_model: str, car_year: int) -> dict:
    """Calculates insurance premium based on car model and year."""
    print(f"--- Tool: calculate_premium called for {car_model} ({car_year}) ---")
    
    try:
        current_year = datetime.now().year
        age = current_year - car_year
        premium = 5000 + (age * 200)

        return {
            "status": "success",
            "car_model": car_model,
            "car_year": car_year,
            "premium": premium,
            "message": f"The estimated premium for your {car_model} for one year is ₹{premium}"
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error in premium calculation: {str(e)}"
        }

# --- Agent that uses the tool ---
premium_agent = Agent(
    name="premium_calculator",
    model="gemini-1.5-flash",
    description="Agent that calculates car insurance premium.",
    instruction="""
You are a premium calculator for car insurance.

When a user gives their car model and manufacturing year:
- Use the `calculate_premium` tool to compute the premium
- Format and display the result clearly

If any input is missing, ask the user to provide it.
""",
    tools=[calculate_premium]
)
