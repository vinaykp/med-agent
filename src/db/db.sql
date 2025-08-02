CREATE TABLE IF NOT EXISTS patients (
    name TEXT PRIMARY KEY,
    data TEXT
);

CREATE TABLE IF NOT EXISTS chat_history (
    id TEXT PRIMARY KEY,
    patient_name TEXT,
    sender TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO patients (name, data)
VALUES ('Sam smith', 
'{
        "Name": "Sarah Smith",
        "Age": 32,
        "Gender": "Female",
        "Patient ID": "P654321",
        "Blood Group": "A+",
        "Allergies": "Penicillin",
        "Diagnosis": "Asthma",
        "Last Visit": "2025-07-10",
        "Vitals": {
            "Blood Pressure": "118/76 mmHg",
            "Heart Rate": "72 bpm",
            "Respiratory Rate": "18 breaths/min",
            "Temperature": "98.4 °F",
            "Oxygen Saturation": "99%",
            "Height": "165 cm",
            "Weight": "60 kg",
            "BMI": "22.0"
        },
        "Contacts": {
            "Primary": "+1-555-7890",
            "Address": "456 Oak Ave, Rivertown",
            "Emergency": "+1-555-3333 (Tom Smith)"
        },
        "Medications": [
            "Albuterol Inhaler - As needed",
            "Montelukast 10mg - Daily"
        ],
        "Family History": {
            "Father": "Asthma",
            "Mother": "None",
            "Siblings": "1 (Asthma)"
        },
        "Visit History": [
            "2025-07-10: Follow-up",
            "2025-04-01: Acute episode",
            "2024-11-20: Initial visit"
        ],
        "Lab Results": {
            "CBC": "Normal",
            "IgE": "Elevated",
            "Spirometry": "Mild obstruction"
        },
        "Billing": {
            "Last Bill": "$200",
            "Outstanding": "$50",
            "Insurance": "Yes"
        }
    }');

INSERT INTO patients (name, data) 
VALUES ('Any Doe', 
'{
        "Name": "John Doe",
        "Age": 45,
        "Gender": "Male",
        "Patient ID": "P123456",
        "Blood Group": "O+",
        "Allergies": "None",
        "Diagnosis": "Hypertension",
        "Last Visit": "2025-06-15",
        "Vitals": {
            "Blood Pressure": "130/85 mmHg",
            "Heart Rate": "78 bpm",
            "Respiratory Rate": "16 breaths/min",
            "Temperature": "98.6 °F",
            "Oxygen Saturation": "97%",
            "Height": "175 cm",
            "Weight": "78 kg",
            "BMI": "25.5"
        },
        "Contacts": {
            "Primary": "+1-555-1234",
            "Address": "123 Main St, Springfield",
            "Emergency": "+1-555-5678 (Jane Doe)"
        },
        "Medications": [
            "Amlodipine 5mg - Daily",
            "Metformin 500mg - Daily",
            "Aspirin 75mg - As needed"
        ],
        "Family History": {
            "Father": "Hypertension",
            "Mother": "Type 2 Diabetes",
            "Siblings": "None"
        },
        "Visit History": [
            "2025-06-15: Routine Checkup",
            "2025-03-10: Follow-up",
            "2024-12-01: Initial Consultation"
        ],
        "Lab Results": {
            "CBC": "Normal",
            "Lipid Profile": "Borderline",
            "Blood Sugar": "110 mg/dL"
        },
        "Billing": {
            "Last Bill": "$120",
            "Outstanding": "$0",
            "Insurance": "Yes"
        }
    }');

    