import json
import os
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

#since there is err i have used direct method rather than importing
# load_dotenv()
# key = os.getenv("OPENAI_API_KEY")

key=""

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-4o-mini",temperature=0.7)

TEMP="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""
prompt=PromptTemplate(
    input=["text","number","subject","tone","response_json"],
    template=TEMP
)
chain=LLMChain(llm=llm,prompt=prompt,output_key="quiz",verbose=True)


TEMP2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
prompt2=PromptTemplate(
    input=["subject","quiz"],
    template=TEMP2
)
chain2=LLMChain(llm=llm,prompt=prompt2,output_key="review",verbose=True)


seq_chain=SequentialChain(
    chains=[chain, chain2],
    input_variables=["text", "number", "subject", "tone", "response_json"], 
    output_variables=["quiz", "review"], 
    verbose=True
)