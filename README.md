# VisionairyTest
Goal: The goal of this repository was to imitate the core functionalities of Visionairy's AI-processing.

Essentially, this is a Python project that uses an open-source LLM API (in this case Groq) to read opthalmology clinical notes and flag patietns who may need tests or procedures. For example, flags I tested for were visual field tests, SLT, punctal occlusion, and toric IOL. An evaluation script measures the precision and recall against a pre-determined answer key.

It's important to note that all of the "patient_00x" text files are self-fabricated and the criteria/flags are simplified and based on amateur research. Also, because my project uses a free API and is not HIPPA-compliant, real patient files should NOT be inputted in the program.

In order to run the program, clone this repository by using Git. 

1) Go to Groq (at console.groq.com) and create an account to obtain your own API key and paste it into the .env file. 

2) Run the following commands in Windows PowerShell or the terminal of your IDE (which can run Python). These commands will set up the appropriate virtual environment to run the program. 

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3) Run the following commands. The flagger program will look through the provided patient files in the "notes" folder and run them through the Groq API, rewriting the results.json file accordingly. The evalute program will score the results against the expected output in expected.json.

python flagger.py
python resutls.json
