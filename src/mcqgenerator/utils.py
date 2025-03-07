import os
import json
import PyPDF2
import traceback
import re

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("Error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Unsupported file format. Only PDF and text files are supported."
        )

def get_table_data(quiz_str):
    try:
        if not quiz_str or quiz_str.strip() == "":
            raise ValueError("Empty quiz string")
        
        # Log the quiz_str for debugging
        print(f"Quiz String: {quiz_str}")
        
        # Clean up the quiz_str to remove extra formatting
        quiz_str = quiz_str.replace("RESPONSE_JSON", "").strip()
        quiz_str = quiz_str.strip("```").strip()
        quiz_str = quiz_str.replace('"',"").strip()
        quiz_str = re.sub(r'\"([^\"]*)\"', r'\\\"\1\\\"', quiz_str)

        # Replace single quotes with double quotes
        quiz_str = quiz_str.replace("'", "\"")

        # Log the cleaned quiz_str for debugging
        print(f"\n\n\nCleaned Quiz String: {quiz_str}\n\n\n")

        # Convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)

        print(f"\n\n\nQuiz Dict: {quiz_dict}\n\n\n") # Debug logging

        quiz_table_data = []
        
        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = ' || '.join(
                [
                    f'{option} -> {option_value}' for option, option_value in value['options'].items()
                ]
            )
            
            correct = value['correct']
            quiz_table_data.append({'MCQ': mcq, 'Options': options, 'Correct': correct})
        
        print(f"\n\n\nQuiz Table Data: {quiz_table_data}\n\n\n") # Debug logging

        return quiz_table_data
        
    except json.JSONDecodeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise ValueError("Invalid JSON format in quiz string")
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None