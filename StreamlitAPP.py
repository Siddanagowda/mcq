import json
import os
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import seq_chain
from langchain.callbacks import get_openai_callback

with open(r'C:\Users\siddana gowda\mcq\Response.json') as file:
    RESPONSE_JSON=json.load(file)

st.title("MCQ Generator")

with st.form("user inputs"):

    uploaded_file = st.file_uploader("Choose a file")

    mcq_count=st.number_input("Enter the number of MCQs",min_value=3,max_value=10)

    subject=st.text_input("Enter the subject",max_chars=20)
    
    tone=st.selectbox("Select the tone",["simple","hard"])

    button=st.form_submit_button("Generate MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text=read_file(uploaded_file)
            
            with get_openai_callback() as cb:
                response=seq_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":RESPONSE_JSON
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error occured. Please try again")

        else:
            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Prompt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}") 

            if isinstance(response,dict):
                quiz=response.get("quiz",None)
                if quiz is not None:
                    table_data=get_table_data(quiz)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index+=1
                        st.table(df)
                        st.text_area(label="Review",value=response.get("review",""))
                    else:
                        st.error("Error in table data")
            else:
                st.write(response)