import json
import logging
import google.generativeai as genai
from typing import Dict, Any

logger = logging.getLogger("gemini_evaluator")

def evaluate_resume_with_llm(raw_text: str, job_description: str, api_key: str) -> Dict[str, Any]:
    if not api_key:
        return {"score": 0, "feedback": "SYSTEM OFFLINE: Missing authorization token."}

    try:
        genai.configure(api_key=api_key)
        model_name = 'models/gemini-2.5-flash' 
        
        system_instruction = (
            "You are an uncompromising legacy corporate Applicant Tracking System (ATS). "
            "Parse the candidate's resume text against the target Job Description. "
            "You must return EXACTLY a valid JSON object matching this exact schema:\n"
            "{\n"
            '  "score": <integer 0-100>,\n'
            '  "feedback": "<string: A brutal, highly specific 3-4 sentence parsing error log. You MUST explicitly point out rigid parser failures such as: spacing/case mismatches (e.g., \\\'TEAM WORK\\\' vs \\\'Teamwork\\\'), keywords found in the wrong section (e.g., \\\'CLOUD\\\' found in certifications but not in skills/experience), unrecognized fancy heading names causing section drops, and explicit missing keywords. Act like a dumb, rigid database.>",\n'
            '  "found_keywords": ["keyword1", "keyword2"],\n'
            '  "missing_keywords": ["missing1", "missing2"],\n'
            '  "optimized_corrections": "<string: A LONG, fully rewritten, elite-level, highly detailed optimized version of the candidate\\\'s resume experience and project descriptions that seamlessly bakes in ALL missing keywords to pass future scans cleanly. Do not hold back on length or detail here.>"\n'
            "}\n"
            "If they miss keywords, populate the missing_keywords list. Always write a comprehensive, detailed optimized_corrections string."
        )
        
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"TARGET JOB DESCRIPTION:\n{job_description}\n\nCANDIDATE RESUME TEXT:\n{raw_text}"
        response = model.generate_content(prompt)
        response_text = str(response.text).strip()
        
        return json.loads(response_text)

    except json.JSONDecodeError:
        logger.error("LLM Schema violation detected.")
        return {
            "score": 0,
            "feedback": "CRITICAL FORMATTING ERROR: The document structure caused a database collision.",
            "found_keywords": [],
            "missing_keywords": ["Critical formatting error during extraction"],
            "optimized_corrections": "System failed to parse text."
        }
    except Exception as e:
        logger.error(f"API Interface failure: {str(e)}")
        return {
            "score": 0,
            "feedback": f"SYSTEM CORRUPTION: API offline. {str(e)}",
            "found_keywords": [],
            "missing_keywords": ["API connection offline"],
            "optimized_corrections": f"Error: {str(e)}"
        }