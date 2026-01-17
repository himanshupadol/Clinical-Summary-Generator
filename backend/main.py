import os
import pandas as pd
from services.llm_service import generate_clinical_summary

# find folder named "data" in current working directory
DATA_DIR = os.path.join(os.getcwd(), "data")

# find and load the csv files in "data" folder
def load_csv(file_name: str) -> pd.DataFrame:
    file_path = os.path.join(DATA_DIR, file_name)

    # finding
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing required data file: {file_name}")
    
    # loading
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read {file_name}: {str(e)}")
    
    if df.empty:
        raise ValueError(f"{file_name} is empty")
    
    return df

# verifying columns in the csv data file
def column_check(df: pd.DataFrame, required_columns: list, file_name: str):
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(f"{file_name} is missing required columns: {missing_columns}")

# loading the primary diagnosis data file
def load_diagnoses() -> pd.DataFrame:
    file_name = "diagnoses.csv"
    required_columns = ["patient_id", "episode_id", "diagnosis_description", "diagnosis_code",]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# loading the medications data
def load_medications() -> pd.DataFrame:
    file_name = "medications.csv"
    required_columns = ["patient_id", "episode_id", "medication_name", "frequency", "reason", "classification",]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# loading the vitals data
def load_vitals() -> pd.DataFrame:
    file_name = "vitals.csv"
    required_columns = ["patient_id", "episode_id", "visit_date", "vital_type", "reading", "min_value", "max_value"]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# loading the wounds data
def load_wounds() -> pd.DataFrame:
    file_name = "wounds.csv"
    required_columns = ["patient_id", "episode_id", "description", "location", "onset_date", "visit_date",]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# loading the oasis data
def load_oasis() -> pd.DataFrame:
    file_name = "oasis.csv"
    required_columns = ["patient_id", "assessment_date", "assessment_type", "grooming", "bathing", "toilet_transfer", "transfer", "ambulation",]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# loading the notes data
def load_notes() -> pd.DataFrame:
    file_name = "notes.csv"
    required_columns = ["patient_id", "episode_id", "note_date", "note_type", "note_text",]

    df = load_csv(file_name)
    column_check(df, required_columns, file_name)

    return df

# retrieving latest data of vitals checkup
def latest_vitals(patient_id: str):
    df = load_vitals()
    patient_df = df[df["patient_id"] == patient_id].copy()
    if patient_df.empty:
        return None
    
    patient_df["visit_date"] = pd.to_datetime(patient_df["visit_date"])
    latest_date = patient_df["visit_date"].max()
    vitals_df = patient_df[patient_df["visit_date"] == latest_date]
    vitals_list = vitals_df[['vital_type', 'reading']].to_dict(orient="records")

    return {"latest_visit_date": latest_date.strftime('%Y-%m-%d'), "vitals": vitals_list}

def latest_wounds(patient_id: str):
    df = load_wounds()
    patient_df = df[df["patient_id"] == patient_id].copy()
    if patient_df.empty:
        return None
    
    patient_df["visit_date"] = pd.to_datetime(patient_df["visit_date"])
    latest_date = patient_df["visit_date"].max()
    wounds_df = patient_df[patient_df["visit_date"] == latest_date]
    wounds_list = wounds_df[['description', 'location', 'onset_date']].to_dict(orient="records")
 
    return {"latest_visit_date": latest_date.strftime('%Y-%m-%d'), "wounds": wounds_list}

def latest_notes(patient_id: str):
    df = load_notes()
    patient_df = df[df["patient_id"] == patient_id].copy()
    if patient_df.empty:
        return None
    patient_df["note_date"] = pd.to_datetime(patient_df["note_date"]) [cite: 18]
    latest_date = patient_df["note_date"].max()
    notes_list = patient_df[patient_df["note_date"] == latest_date]['note_text'].tolist()
    return {"latest_note_date": latest_date.strftime('%Y-%m-%d'), "notes": notes_list}

def get_medications(patient_id: str):
    df = load_medications()
    patient_df = df[df["patient_id"] == patient_id]
    if patient_df.empty:
        return []
    return patient_df[["medication_name", "frequency", "reason"]].to_dict(orient="records") [cite: 20]

def get_oasis(patient_id: str):
    df = load_oasis()
    patient_df = df[df["patient_id"] == patient_id]
    if patient_df.empty:
        return []
    return patient_df.drop_duplicates().to_dict(orient="records") [cite: 21]


def build_llm_context(patient_id: str) -> str:
    context_sections = []

    # Diagnosis 
    try:
        diagnosis = get_primary_diagnosis(patient_id)
        diag_block = "Primary Diagnoses:\n" + "\n".join([f"- {d}" for d in diagnosis])
        context_sections.append(diag_block)
    except:
        context_sections.append("Primary Diagnosis: Not documented.")

    # Vitals 
    vitals_data = latest_vitals(patient_id)
    if vitals_data:
        v_block = f"Recent Vital Signs (Visit: {vitals_data['latest_visit_date']}):\n"
        v_block += "\n".join([f"- {v['vital_type']}: {v['reading']}" for v in vitals_data["vitals"]])
        context_sections.append(v_block)
    else:
        context_sections.append("Recent Vital Signs: No data available.")

    # Wounds
    wounds_data = latest_wounds(patient_id)
    if wounds_data:
        w_block = f"Active Wounds (Latest assessment: {wounds_data['latest_visit_date']}):\n"
        w_block += "\n".join([f"- {w['description']} at {w['location']}" for w in wounds_data["wounds"]])
        context_sections.append(w_block.strip())
    else:
        context_sections.append("Active Wounds:\n- No active wounds documented.")

    # Meds
    meds = get_medications(patient_id)
    if meds:
        m_block = "Current Medications:\n"
        m_block += "\n".join([f"- {m['medication_name']} ({m['frequency']}) for {m['reason']}" for m in meds])
        context_sections.append(m_block.strip())
    else:
        context_sections.append("Current Medications:\n- No medications documented.")
    
    # Notes
    notes_data = latest_notes(patient_id)
    if notes_data:
        n_block = f"Recent Clinical Notes (Date: {notes_data['latest_note_date']}):\n"
        n_block += "\n".join([f"- {note}" for note in notes_data["notes"]])
        context_sections.append(n_block.strip())
    else:
        context_sections.append("Recent Clinical Notes:\n- No recent notes.")
    
    # OASIS
    oasis = get_oasis(patient_id)
    if oasis:
        o = oasis[0] # Taking the most recent assessment
        o_block = (f"Functional Status (Assessment: {o['assessment_type']}):\n"
                   f"- Grooming: {o['grooming']}, Bathing: {o['bathing']}\n"
                   f"- Transfers: {o['transfer']}, Ambulation: {o['ambulation']}")
        context_sections.append(o_block.strip())
    else:
        context_sections.append("Functional Status:\n- No assessment data available.")

    return "\n\n".join(context_sections)

def generate_summary_for_patient(patient_id: str) -> str:
    final_context = build_llm_context(patient_id)
    return generate_clinical_summary(final_context)