# agents.py
from crewai import LLM, Agent
from config import GROQ_API_KEY,GEMINI_API_KEY
import google.generativeai as genai


# Use a smaller model to reduce token usage
llm = LLM(
    model="gemini/gemini-2.5-pro",  # string مباشرة
    api_key=GEMINI_API_KEY,
    max_tokens=2000,
    temperature=0.3
)

def create_travel_planner_agent():
    """Main travel planner agent"""
    return Agent(
        role='Travel Planner Expert',
        goal='Create comprehensive, budget-aware travel plans with flights, hotels, attractions, and restaurants',
        backstory=(
            "You are an experienced travel consultant specialized in creating detailed, personalized travel itineraries. "
            "You excel at finding optimal flights, budget-friendly accommodations, must-see attractions, "
            "and authentic dining experiences. You always respect the client's budget constraints and provide "
            "clear cost breakdowns. You verify all information through reliable sources."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
