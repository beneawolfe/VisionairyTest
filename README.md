# VisionairyTest
Goal: The goal of this repository was to imitate the core functionalities of Visionairy's AI-processing.

Essentially, this is a Python project that uses an open-source LLM API (in this case Groq) to read opthalmology clinical notes and flag patients who may need tests or procedures. For example, flags I tested for were visual field tests, SLT, punctal occlusion, and toric IOL. An evaluation file/script measures the precision and recall against a pre-determined answer key.

It's important to note that all of the "patient_00x" text files are self-fabricated and the criteria/flags are simplified and based on amateur research. Also, because my project uses a free API and is not HIPPA-compliant, real patient files should NOT be inputted in the program.

## Running the Program

### 1. First, clone the repository by using Git. Navigate into the repository.

```
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git 
cd YOUR-REPO-NAME
```

### 2. Get a Groq API key. 

Next, create a free account at [console.groq.com](https://console.groq.com) and generate your unique API key. Then create a file named `.env` in the project folder and paste your key in:

```
GROQ_API_KEY=your_key_here
```

### 3. Set up the virtual environment

Run the following commands in Windows PowerShell or your IDE's terminal. These commands will create and activate a virtual environment, installing the required packages.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> On macOS/Linux, activate with `source venv/bin/activate` instead.

### 4. Run the program
The flagger.py file will read each patient note in the `notes/` folder, send it to teh Groq API to go through the data, and save each evaluated flag to `results.json`. This process overwrites any previous results. `evaluate.py` scores those results against the answer key in `expected.json`, reporting precision, recall, and any mistakes.

```
python flagger.py
python evaluate.py
```
