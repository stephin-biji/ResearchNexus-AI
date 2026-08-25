import os
import json
import re
import time

from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader


# =================================================
# LOAD API KEY
# =================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )


# =================================================
# INITIALIZE GEMINI CLIENT
# =================================================

client = genai.Client(
    api_key=API_KEY
)


# =================================================
# AI MODELS
# =================================================

# Primary model
PRIMARY_MODEL = "gemini-3.6-flash"

# Fallback model if primary model is unavailable
FALLBACK_MODEL = "gemini-2.5-flash"


# =================================================
# PDF TEXT EXTRACTION
# =================================================

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF.
    """

    try:

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:

        raise Exception(
            f"PDF extraction failed: {str(e)}"
        )


# =================================================
# CLEAN AI RESPONSE
# =================================================

def clean_json_response(result_text):
    """
    Clean Gemini response and convert it
    into valid JSON.
    """

    if not result_text:
        raise ValueError(
            "AI returned an empty response."
        )

    result_text = result_text.strip()

    # Remove ```json
    result_text = re.sub(
        r"^```json\s*",
        "",
        result_text,
        flags=re.IGNORECASE
    )

    # Remove ```
    result_text = re.sub(
        r"^```\s*",
        "",
        result_text
    )

    result_text = re.sub(
        r"\s*```$",
        "",
        result_text
    )

    result_text = result_text.strip()

    # Find JSON object if extra text exists
    json_match = re.search(
        r"\{.*\}",
        result_text,
        re.DOTALL
    )

    if json_match:

        result_text = json_match.group()

    return json.loads(result_text)


# =================================================
# CHECK TEMPORARY API ERROR
# =================================================

def is_temporary_error(error_message):
    """
    Check whether an API error is temporary
    and worth retrying.
    """

    temporary_errors = [

        "429",
        "RESOURCE_EXHAUSTED",
        "503",
        "UNAVAILABLE",
        "high demand",
        "timeout",
        "timed out",
        "connection",
        "temporarily unavailable"

    ]

    error_message = error_message.lower()

    return any(
        error.lower() in error_message
        for error in temporary_errors
    )


# =================================================
# GENERATE CONTENT WITH RETRY
# =================================================

def generate_with_retry(
    prompt,
    max_retries=4
):
    """
    Generate AI content with automatic retry.

    First tries the primary model.
    If unavailable, tries fallback model.
    """

    models = [

        PRIMARY_MODEL,
        FALLBACK_MODEL

    ]

    last_error = None

    for model in models:

        for attempt in range(
            max_retries
        ):

            try:

                response = (
                    client.models.generate_content(

                        model=model,

                        contents=prompt

                    )
                )

                if (
                    response
                    and response.text
                ):

                    return response.text

                raise ValueError(
                    "AI returned an empty response."
                )

            except Exception as e:

                last_error = str(e)

                print(
                    f"Attempt {attempt + 1} "
                    f"failed using {model}: "
                    f"{last_error}"
                )

                if not is_temporary_error(
                    last_error
                ):

                    break

                if (
                    attempt
                    < max_retries - 1
                ):

                    # Exponential backoff
                    wait_time = (
                        2 ** attempt
                    )

                    print(
                        f"Waiting {wait_time} seconds "
                        "before retrying..."
                    )

                    time.sleep(
                        wait_time
                    )

        print(
            f"Switching model after failure: "
            f"{model}"
        )

    raise Exception(
        last_error
        or
        "AI generation failed."
    )


# =================================================
# RESEARCH KNOWLEDGE EXTRACTION
# =================================================

def extract_research_knowledge(
    text,
    filename
):
    """
    Use AI to extract entities,
    relationships and research intelligence.
    """

    # Limit text to reduce API usage
    text = text[:10000]

    prompt = f"""
You are an AI research knowledge extraction engine.

Analyze the following university research document.

Filename:
{filename}

Research Content:

{text}


Extract the important research entities,
research topics, technologies, datasets,
methods and relationships.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "document": "{filename}",

    "summary":
    "A short 2-3 sentence summary",

    "entities": [

        {{
            "name": "Entity name",

            "type":
            "Researcher / Department / Topic / Technology / Dataset / Method"
        }}

    ],

    "relationships": [

        {{
            "source": "Entity name",

            "target": "Entity name",

            "relationship":
            "USES / STUDIES / BELONGS_TO / CREATED_BY / RELATED_TO"
        }}

    ],

    "topics": [

        "topic1",

        "topic2"

    ],

    "collaboration_opportunities": [

        "Describe a possible cross-disciplinary collaboration"
    ],

    "redundancy_risk":
    "Low / Medium / High"
}}


RULES:

- Extract only meaningful information.
- Do not invent facts.
- Only use information supported
  by the research content.
- Identify technologies, datasets,
  methods and research topics.
- Identify meaningful relationships.
- Find potential interdisciplinary
  collaboration opportunities.
- Do not return markdown.
- Do not add explanations outside JSON.
- Return valid JSON only.
"""

    try:

        result_text = generate_with_retry(
            prompt
        )

        result = clean_json_response(
            result_text
        )

        return result

    except json.JSONDecodeError:

        return {

            "error":
            "AI returned an invalid JSON response. "
            "Please try analyzing again."

        }

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:

            return {

                "error":
                "Gemini API quota or rate limit has been reached. "
                "Please wait and try again later."

            }

        elif "503" in error_message:

            return {

                "error":
                "The AI model is currently experiencing high demand. "
                "Please try again in a few minutes."

            }

        elif (
            "getaddrinfo"
            in error_message
        ):

            return {

                "error":
                "Network connection error. "
                "Please check your internet connection."

            }

        else:

            return {

                "error":
                f"AI Analysis failed: {error_message}"

            }


# =================================================
# CROSS-RESEARCH AI INTELLIGENCE
# =================================================

def analyze_cross_research_connection(
    paper1,
    paper2,
    shared_entities,
    shared_topics,
    related_concepts
):
    """
    Analyze the relationship between two
    research papers and generate a meaningful
    collaboration insight.
    """

    paper1_name = paper1.get(
        "document",
        "Research Paper 1"
    )

    paper2_name = paper2.get(
        "document",
        "Research Paper 2"
    )

    paper1_summary = paper1.get(
        "summary",
        ""
    )

    paper2_summary = paper2.get(
        "summary",
        ""
    )

    prompt = f"""
You are an AI university research
intelligence system.

Analyze the potential relationship
between two research papers.


PAPER 1

Name:
{paper1_name}

Summary:
{paper1_summary}


PAPER 2

Name:
{paper2_name}

Summary:
{paper2_summary}


SHARED ENTITIES:

{", ".join(shared_entities) if shared_entities else "None"}


SHARED TOPICS:

{", ".join(shared_topics) if shared_topics else "None"}


RELATED RESEARCH CONCEPTS:

{", ".join(related_concepts) if related_concepts else "None"}


Your task:

1. Explain why these papers are connected.
2. Explain how researchers could collaborate.
3. Suggest one combined research idea.
4. Estimate connection strength.


Return ONLY valid JSON.

Use exactly this structure:

{{
    "connection_explanation":
    "Explain clearly why the papers are related.",

    "collaboration_potential":
    "Explain how researchers could collaborate.",

    "combined_research_idea":
    "Describe one possible combined research project.",

    "connection_strength":
    "Low / Medium / High"
}}


RULES:

- Base the answer only on the
  provided information.
- Do not invent research results.
- Be specific.
- Avoid generic statements.
- Do not return markdown.
- Return JSON only.
"""

    try:

        result_text = generate_with_retry(
            prompt
        )

        result = clean_json_response(
            result_text
        )

        return result

    except Exception as e:

        return {

            "connection_explanation":
            "Unable to generate AI connection explanation.",

            "collaboration_potential":
            "AI collaboration analysis is currently unavailable.",

            "combined_research_idea":
            "No combined research idea generated.",

            "connection_strength":
            "Unknown",

            "error":
            str(e)

        }