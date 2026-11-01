
import sys
import os
from dotenv import load_dotenv
from docx import Document
from pypdf import pdfReader
from google import genai


load_dotenv()  # this methods are load the env file variable  and read 


API_KEY=os.getenv("GEMINI_API_KEY","")
MODEL=os.getenv("GEMINI_API_MODEL","gemini-3.6-flash")



REPORT_SECTION=[
    ("strengths","Strengths"),
    ("gaps","Gaps"),
    ("missing_or_weekskills","Missing_or_weekskills"),
    ("improvement_suggestion","Improvement_or_suggestion"),
    ("overall_summary","Overall_Summary")
]

