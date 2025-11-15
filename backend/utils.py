import re
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_pios_for_department(department, df):
    filtered = df[df['Department'] == department]
    return filtered.to_dict('records')

def generate_rti_letter_gpt(user_issue, pio_info, user_name, user_address):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your-openai-api-key-here":
        return """[RTI Letter - OpenAI API Key Required]

To: {pio_authority}
{authority_name}
{department}
{state}

From: {user_name}
Address: {user_address}

Subject: Request for Information under Right to Information Act, 2005

Respected Sir/Madam,

Under the provisions of the Right to Information Act, 2005, I would like to request the following information:

Issue/Query: {user_issue}

I would appreciate if you could provide the requested information at the earliest. If any fees are applicable, please inform me of the amount and payment procedure.

I look forward to your response within the statutory time period of 30 days as mandated under the RTI Act, 2005.

Thank you for your attention to this matter.

Yours faithfully,
{user_name}

Date: [Current Date]

Note: Please configure your OpenAI API key in the backend/.env file to generate AI-powered RTI letters.
""".format(
        pio_authority=pio_info.get('PIO_Authority', 'N/A'),
        authority_name=pio_info.get('Authority_Name', 'N/A'),
        department=pio_info.get('Department', 'N/A'),
        state=pio_info.get('State', 'N/A'),
        user_name=user_name,
        user_address=user_address,
        user_issue=user_issue
    )

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""Generate a formal and polite RTI (Right to Information) letter as per the RTI Act 2005 of India.

User Issue/Query: {user_issue}
Department: {pio_info.get('Department', 'N/A')}
PIO Authority: {pio_info.get('PIO_Authority', 'N/A')}
Authority Name: {pio_info.get('Authority_Name', 'N/A')}
State: {pio_info.get('State', 'N/A')}

User Details:
Name: {user_name}
Address: {user_address}

Please draft a complete formal RTI letter that:
1. Is addressed to the PIO mentioned above
2. References the RTI Act 2005
3. Clearly states the information being requested based on the user's issue
4. Includes proper formatting with To, From, Subject, and Date fields
5. Is polite and professional in tone
6. Mentions the 30-day statutory time period
7. Ends with proper salutation

Format the letter professionally and ensure it is ready to be sent."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert legal assistant who drafts formal RTI letters according to the Right to Information Act, 2005 of India."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating letter: {str(e)}\n\nPlease ensure your OpenAI API key is properly configured in the backend/.env file."
