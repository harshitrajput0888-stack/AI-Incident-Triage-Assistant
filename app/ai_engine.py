from huggingface_hub import InferenceClient

from app.config import HF_TOKEN


class AIIncidentAnalyzer:

    def __init__(self):

        self.client = InferenceClient(
            token=HF_TOKEN
        )

    def analyze(self, incident, triage_result):

        prompt = f"""
You are an experienced IT incident management assistant.

Analyze the following IT incident.

Incident Title:
{incident["title"]}

Incident Description:
{incident["description"]}

Affected Service:
{incident["affected_service"]}

Affected Users:
{incident["affected_users"]}

Environment:
{incident["environment"]}

Python Triage Result:
Category: {triage_result["category"]}
Severity: {triage_result["severity"]}
Priority: {triage_result["priority"]}

Provide a practical incident analysis with these sections:

1. Probable Root Cause
2. Immediate Actions
3. Investigation Steps
4. Business Impact
5. Prevention Recommendations

Do not invent facts that are not available.
Keep the response concise and professional.
"""

        try:

            response = self.client.chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an IT incident triage "
                            "and application support assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="meta-llama/Llama-3.1-8B-Instruct",
                max_tokens=500,
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as error:

            return f"AI analysis failed: {error}"