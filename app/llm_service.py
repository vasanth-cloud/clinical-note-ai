import httpx
import json
import re
import os

OPENROUTER_API_KEY = "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"

async def llm_primary_analysis(text: str) -> dict:
    """LLM-first analysis with healthcare AI personality"""
    
    # Casual chat detection
    casual_keywords = ['how are you', 'hi', 'hello', 'what is', 'vasanth']
    if any(keyword in text.lower() for keyword in casual_keywords):
        return {
            "subjective": "Healthcare AI conversation",
            "objective": "User interaction detected",
            "assessment": "Clinical Note AI ready",
            "plan": "Please provide clinical notes",
            "medications": [],
            "vitals": []
        }
    
    try:
        prompt = f"""Extract SOAP clinical notes from:

{text}

Return ONLY JSON:
{{"subjective": "Patient symptoms", "objective": "Exam findings", "assessment": "Diagnosis", "plan": "Treatment", "medications": []}}"""

        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                }
            )
            
            content = response.json()["choices"][0]["message"]["content"]
            json_str = re.sub(r'```json|```', '', content).strip()
            return json.loads(json_str)
            
    except Exception:
        return {
            "subjective": text[:200] + "...",
            "objective": "Clinical data extraction",
            "assessment": "Pending analysis",
            "plan": "Processing complete",
            "medications": [],
            "vitals": []
        }
