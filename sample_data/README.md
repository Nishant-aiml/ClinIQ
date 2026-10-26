# ClinIQ Sample Clinical Test Data

This directory contains authentic sample clinical documents (PDFs) and medical document images (PNG/JPEG) designed for testing ClinIQ's multi-modal ingestion pipeline, OCR extraction, timeline reconstruction, and clinical intelligence engines.

---

## 1. Directory Structure

```
sample_data/
├── pdfs/
│   ├── Complete_Blood_Count_CBC_Report.pdf        # Hematology lab report (Hb, RBC, WBC, Ferritin)
│   ├── Comprehensive_Metabolic_Panel_CMP.pdf      # Metabolic & renal panel (Glucose, HbA1c, eGFR, Lipids)
│   ├── Cardiology_Clinical_Consultation_Note.pdf  # Outpatient cardiology examination & ECG note
│   └── Discharge_Summary_Hospital_Stay.pdf        # Inpatient discharge summary (DKA / Hypertensive Urgency)
│
└── images/
    ├── Lab_Report_Scan_Hematology_CBC.png         # Scanned laboratory report image for OCR testing
    ├── Diagnostic_Chemistry_Panel_Scan.png        # Scanned biochemistry & metabolic report image
    ├── Digital_Medical_Report_Screen.png          # Screen capture of clinical diagnostics
    ├── Clinical_Prescription_Slip_Rx.jpeg         # Handwritten / printed outpatient prescription slip
    ├── Hospital_Vitals_Summary_Sheet.jpeg         # Inpatient nursing vitals tracking sheet
    └── Patient_Outpatient_Prescription.jpeg       # Outpatient pharmacy prescription order
```

---

## 2. Test Files Breakdown

| File Name | Category | Patient / Target | Key Parameters / Clinical Features |
| :--- | :--- | :--- | :--- |
| **`Complete_Blood_Count_CBC_Report.pdf`** | Lab Report | Priya Sharma | Hemoglobin (10.4 g/dL, LOW), RBC (3.65, LOW), Ferritin (18.2 ng/mL, LOW). Tests anemia flag detection. |
| **`Comprehensive_Metabolic_Panel_CMP.pdf`** | Lab Report | Elena Rostova | Glucose (164 mg/dL, HIGH), HbA1c (8.2%, HIGH), BUN (26.4, HIGH), Creatinine (1.38 mg/dL, HIGH), eGFR (51, LOW). Tests CKD Stage 3a and Diabetes flags. |
| **`Cardiology_Clinical_Consultation_Note.pdf`** | Clinical Note | Arjun Mehta | Annual cardiac exam, ECG normal sinus rhythm, 5-year longitudinal stability, ASCVD risk &lt; 2.5%. |
| **`Discharge_Summary_Hospital_Stay.pdf`** | Discharge Summary | Priya Sharma | Hypertensive urgency, acute renal exacerbation, discharge medications (Metformin, Lisinopril, Amlodipine, Atorvastatin). |
| **`Lab_Report_Scan_Hematology_CBC.png`** | Image OCR | Diagnostic Scan | Tests multi-modal image OCR and tabular lab extraction from image. |
| **`Clinical_Prescription_Slip_Rx.jpeg`** | Prescription Image | Prescription Slip | Tests OCR extraction of prescription drugs, dosing, and frequencies from photos/scans. |

---

## 3. How to Use for Testing

### Option A: Via the ClinIQ Web Interface
1. Log into ClinIQ at `http://localhost:3056` (or via Ngrok URL `https://charging-lend-scoff.ngrok-free.dev`).
2. Navigate to **Patients** and select any patient (e.g. *Priya Sharma* or *Arjun Mehta*).
3. Click **Upload Document** or drag-and-drop any PDF from `sample_data/pdfs/` or image from `sample_data/images/`.
4. ClinIQ will automatically parse the document via OCR, extract structured lab parameters, vitals, or medications, and populate the patient's:
   - **Clinical Timeline**
   - **Longitudinal Analytics Charts**
   - **Organ System Health Scores** (Renal, Cardiovascular, Metabolic)
   - **AI Copilot Context**

### Option B: Via Direct Backend API (`curl` / Swagger)
```bash
curl -X POST "http://localhost:8056/api/v1/ingestion/patients/{patient_id}/upload" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -F "file=@sample_data/pdfs/Complete_Blood_Count_CBC_Report.pdf"
```
Or open interactive API docs at `http://127.0.0.1:8056/docs`.