from dotenv import load_dotenv
from google import genai
from typing import Literal
from pydantic import BaseModel
import json

load_dotenv()

client = genai.Client()

class TriageResultFormat(BaseModel):
    summary : str
    category : Literal["billing", "technical", "account", "general"]
    priority : Literal["low", "medium", "high", "critical"]

class Ticket:
    def __init__(self, text):
        self.text = text
        self.triage_result = None

    def triage(self):
        prompt = f"""
        Analyse this ticket:
        {self.text}
        return the result as JSON.
        """
        response = client.models.generate_content(
            model = "gemini-3.1-flash-lite",
            contents = prompt,
            config = {"response_mime_type" : "application/json",
                     "response_schema" : TriageResultFormat}
        )

        self.triage_result = TriageResultFormat.model_validate_json(response.text)
        return self.triage_result


ticket1 = Ticket("I was charged twice")
ticket2 = Ticket("The website is down")
ticket3 = Ticket("I want to change my profile picture")

tickets = [ticket1, ticket2, ticket3]

for index, ticket in enumerate(tickets, start=1):
    result = ticket.triage()

priority_rank = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3
}

prioritized_results = sorted(
    tickets,
    key=lambda ticket: priority_rank[ticket.triage_result.priority]
    )

for index, results in enumerate(prioritized_results, start=1):
    print(f"Ticket{index}")
    print(f"summary: {results.triage_result.summary}")
    print(f"category: {results.triage_result.category}")
    print(f"priority: {results.triage_result.priority}\n")