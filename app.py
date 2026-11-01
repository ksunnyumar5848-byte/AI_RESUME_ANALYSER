
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


def extract_resume_text(uploaded_file):

    """ Return the plain text of the uploaded file like pdf or docx file """

    file_name=uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        reader=pdfReader(uploaded_file)

        pages=[]

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return '\n'.join(pages).strip()

    if file_name.endswith(".docx"):
       document=Document(uploaded_file) 

       Paragraphs=[]

       for p in document.Paragraphs:
           Paragraphs.append(p.text or "")

       return '\n'.join(Paragraphs).strip()   


    return "NO INPUT WAS GIVIN AS CV aks user for it "  





# this methods are analyze resume


def analyze_resume(resume_text,job_description):
    """LLM CALL NUMBER 1 TRUN  the resume and JD structure JSON """

    client =genai.Client.models(API_KEY)

    instructions="""     you compare against job descriptions .. 

    Relpy with json only using exactly there key every value is a list of sort string 

    {
      "candidate_skills" :[],
      "candidate_expreience:[],
      "candidate_qualification":[],
      "required_skills":[],
      "preferred_skills":[],
      "matching_skills":[],
      "missing_skills":[],
      "gaps":[]
    }


    Rules:
    - use only information that actually appears in the resume or the job description 
    -Never invent skills ,employers, job description , dates .etc,
    -"missing skills" means the job description aks for and the resume does not mention it 
    -level a list empty when the text gives you nothing to put it 

"""


