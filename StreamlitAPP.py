import os

# Unset the SSL_CERT_FILE environment variable
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]

import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import seq_chain
from langchain_community.callbacks.manager import get_openai_callback
from fpdf import FPDF  # Import the FPDF library

with open(r'C:\Users\siddana gowda\mcq\Response.json') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator")

with st.form("user inputs"):

    uploaded_file = st.file_uploader("Choose a file")

    mcq_count = st.number_input("Enter the number of MCQs", min_value=3, max_value=10)

    subject = st.text_input("Enter the subject", max_chars=20)
    
    tone = st.selectbox("Select the tone", ["simple", "hard"])

    button = st.form_submit_button("Generate MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(uploaded_file)
            
            with get_openai_callback() as cb:
                response = seq_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": RESPONSE_JSON
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error occurred. Please try again")

        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}") 

            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    print(f"Quiz: {quiz}")  # Debug logging
                    table_data = get_table_data(quiz)
                    if table_data:
                        df = pd.DataFrame(table_data)
                        df.index += 1
                        st.table(df)
                        st.text_area(label="Review", value=response.get("review", ""))

                        # Add a button to download the MCQs as a PDF
                        def generate_pdf(dataframe):
                            pdf = FPDF()
                            pdf.set_auto_page_break(auto=True, margin=15)
                            pdf.add_page()
                            pdf.set_font("Arial", size=12)

                            pdf.cell(200, 10, txt="Generated MCQs", ln=True, align="C")
                            pdf.ln(10)

                            for index, row in dataframe.iterrows():
                                pdf.multi_cell(0, 10, txt=f"Q{index}: {row['MCQ']}")
                                pdf.multi_cell(0, 10, txt=f"Choices: {row['Choices']}")
                                pdf.multi_cell(0, 10, txt=f"Correct Answer: {row['Correct']}")
                                pdf.ln(5)

                            return pdf.output(dest="S").encode("latin1")

                        pdf_data = generate_pdf(df)
                        st.download_button(
                            label="Download MCQs as PDF",
                            data=pdf_data,
                            file_name="mcqs.pdf",
                            mime="application/pdf",
                        )
                    else:
                        st.error("Error in table data")
                else:
                    st.error("Quiz data is missing in the response")
            else:
                st.write(response)