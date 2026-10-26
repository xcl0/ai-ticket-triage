from typing import Literal
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel

load_dotenv()

class TriageResult(BaseModel):
    summary: str
    category: Literal["billing", "technical", "account", "general"]
    priority: Literal["low", "medium", "high", "critical"]
    assigned_team: Literal[
        "billing_support",
        "technical_support",
        "account_support",
        "general_support",
    ]
    reason: str

client = genai.Client()

def triage_ticket(ticket):
    prompt = f"""
    Analyze the following support ticket and classify it.

    Use these exact priority rules:
    - low: A question or minor inconvenience. Nothing important is blocked.
    - medium: A feature is broken, but the user has a reasonable workaround.
    - high: An important function is blocked and no reasonable workaround exists.
    - critical: A widespread outage, active security breach, or immediate severe risk.

    Use these exact category and team rules:
    - billing: Charges, payments, invoices, subscriptions, or refunds.
      Assign to billing_support.
    - technical: Broken features, errors, outages, or performance problems.
      Assign to technical_support.
    - account: Login, password, profile, account settings, or account security.
      Assign to account_support.
    - general: Questions that do not fit the other categories.
      Assign to general_support.

    Judge priority based on actual impact, not emotional or urgent wording.

    Ticket:
    {ticket}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": TriageResult
            }
        )

    except errors.APIError as error:
        if error.code == 503:
            raise RuntimeError("Gemini is temporarily overloaded. Please try again later.")
        elif error.code == 429:
            raise RuntimeError("The API usage limit has been reached. Please try again later.")
        elif error.code in {401, 403}:
            raise RuntimeError("The Gemini API key is invalid or unauthorized.")
        else:
            raise RuntimeError(f"Gemini API error: {error.message}")

    return TriageResult.model_validate_json(response.text)