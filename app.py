
import sys
import os
from dotenv import load_dotenv
from docx import Document
from pypdf import pdfReader
from google import genai
import json


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

    client =genai.Client(api_key=API_KEY)

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
    user_messages= f"""
                     Compare this resume aginst this job description and relpy with the json 

                     RESUME:{resume_text}

                     JOB_DESCRIPTION:

                     {job_description}

"""
    response = client.models.generate_content(
         model=MODEL,
         contents=f"""
           Instructions:{instructions}
           User Message: {user_messages}
          """,
         config={
            "response_mime_type": "application/json"}
        )

    result = json.loads(response.text)

    return result




# this are genrate the final output 


def generate_final_report(structured_analysis):

    clinet= genai.Client(api_key=API_KEY)

    instructions = """You write short, honest resume feedback for a candidate.
    
    You receive JSON that was built from a resume and a job description.
    Reply with JSON only, using exactly these keys. Every value is a string.
    
    {
      "strengths": "",
      "gaps": "",
      "missing_or_weak_skills": "",
      "improvement_suggestions": "",
      "overall_summary": ""
    }
    
    Rules:
    - Write the first four values as Markdown bullet lists, one point per line ("- point").
    - Write "overall_summary" as one short paragraph.
    - Never leave a value empty. If a section has nothing to report, say so in one bullet,
      such as "- Nothing further was identified from the provided resume."
    - Put specific tools and technologies in "missing_or_weak_skills", and put experience,
      qualifications and responsibilities in "gaps", so the two do not repeat each other.
    - Base everything on the JSON you are given, and do not invent anything new.
    - Never use the words "lacks", "lacking", "no experience", "no exposure",
      "does not know" or "does not have" anywhere, including the overall summary.
      You only know what this one resume mentions, not what the candidate can really do.
      Write "Apache Airflow was not identified in the provided resume" and
      "The resume does not show the 3+ years of analytics experience the role asks for".
    - Do not give a numeric score or a percentage.
"""

    user_message=f"""
                   trun this structured data into resume feedback and reply with json 
                   {json.dumps(structured_analysis,indent=2)}
    """

    response =  clinet.models.generate_content(
             model=MODEL,
             contents=f"""
               Instructions:{instructions}
               User Message: {user_message}
              """,
             config={
                "response_mime_type": "application/json"}
            )
    
    report = json.loads(response.text)


    for key,_ in REPORT_SECTION:
        value=report.get(key)

        if isinstance(value,list):
            value="\n".join("-" + str(point) for point in value)

        report[key]=value or "Nothing was reported for this section "
    return report


def create_dwonloadable_report(final_report):
    """
       build the work down text for resume_analayzer download

    """

    lines=["resume Analysis"]

    for key, heading in REPORT_SECTION:
        lines.append(f"# {heading}")
        lines.append(final_report)
    return "\n \n ".join(lines)    





     

    
    