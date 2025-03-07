# MCQ Generator

MCQ Generator is a Python-based application that generates multiple-choice questions (MCQs) from a given text file. It uses OpenAI's GPT-4 model to create the questions and Streamlit for the web interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [License](#license)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Siddanagowda/mcq-generator.git
cd mcq
```

2. Create a virtual environment and activate it:

```sh
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage
1. Set up your OpenAI API key:

Create a .env file in the root directory of the project.

Add your OpenAI API key to the .env file:

```sh
OPENAI_API_KEY=your_openai_api_key
```


2. Run the Streamlit application:

```sh
streamlit run StreamlitAPP.py
```

3. Open your web browser and go to http://localhost:8501 to access the MCQ Generator application.

4. Upload a text file, specify the number of MCQs, subject, and tone, and click the "Generate MCQs" button to generate the questions.

## Project Structure
```sh
mcq-generator/
│
├── .env
├── .gitignore
├── [data.txt]
├── [README.md]
├── [requirements.txt]
├── [Response.json]
├── [setup.py]
├── [StreamlitAPP.py]
├── [test.py]
├── env/
│   ├── ...
│
├── experiment/
│   ├── [mcq.ipynb]
│   ├── [quiz.csv]
│
├── logs/
│   ├── ...
│
├── [mcqgenrator.egg-info]
│   ├── [dependency_links.txt]
│   ├── PKG-INFO
│   ├── [requires.txt]
│   ├── [SOURCES.txt]
│   ├── [top_level.txt]
│
├── src/
│   ├── [__init__.py]
│   ├── mcqgenerator/
│       ├── [__init__.py]
│       ├── [logger.py]
│       ├── [MCQGenerator.py]
│       ├── [utils.py]

```

## Configuration

1. **Response.json:** Template for the MCQ responses.
2. **data.txt**: Sample data file used for generating MCQs.
3. **StreamlitAPP.py**: Main entry point for the Streamlit application.
4. **src/mcqgenerator/MCQGenerator.py**: Contains the logic for generating MCQs using LangChain.
5. **src/mcqgenerator/utils.py**: Utility functions for reading files and formatting data.
6. **src/mcqgenerator/logger.py**: Logging configuration.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

```sh
This README.md file provides an overview of the project, including installation instructions, usage guidelines, project structure, and configuration details. Adjust the content as needed to fit your specific project requirements.
```