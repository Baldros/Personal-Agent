from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

# Carregando api keys
load_dotenv()

api_key = os.getenv("GOOGLE_KEY")

# Using Google AI Studio
agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=api_key),
    markdown=True,
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")