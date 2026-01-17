# Clinical Summary Generator
An AI-powered application built with Streamlit that generates concise, evidence-based clinical summaries for patients by processing various medical data points.

## Project Structure
clinical_summary_generator/
├── app/
│   └── app.py              # Streamlit frontend with custom styling
├── backend/
│   └── main.py             # Data processing & clinical context building
├── services/
│   └── llm_service.py      # Hugging Face Router API integration
├── data/                   # Clinical CSV files (diagnoses, meds, notes, etc.)
├── VEHP/                   # Project Virtual Environment (Isolated workspace)
├── requirements.txt        # Project dependencies
└── .gitignore              # Excludes VEHP and sensitive files from version control

## Features
Patient-Centric Search: Quickly retrieve data using specific Patient IDs.

Automated Context Building: Aggregates diagnosis, vital signs, medication history, clinical notes, and functional status (OASIS) into a unified prompt.

AI Summarization: Leverages the google/flan-t5-large model via the Hugging Face Router for factual, clinically-formatted summaries.

Modern UI: Features a clean, two-column interface with a customized "Generate Summary".

## Setup & Installation
### 1. Environment Setup
#### 1.1 Create the Environment
python -m venv VEHP

#### 1.2 Activate the Environment
VEHP\Scripts\activate # for Windows
source VEHP/bin/activate # for macOS/Linux

### 2. Clone the repository:
git clone <your-repo-url>
cd clinical_summary_generator

### 3. Install dependencies:
pip install -r requirements.txt

### 4. Configure Secrets:
Create a .streamlit/secrets.toml file and add your Hugging Face API token:
HF_TOKEN = "your_huggingface_token_here"

### 5. Run the application:
python -m streamlit run app/app.py