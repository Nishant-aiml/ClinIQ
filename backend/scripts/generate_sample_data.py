"""
ClinIQ — Sample Data Generator.
Creates authentic clinical test PDFs and copies sample medical images into `sample_data/`.
"""
import os
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_DIR = ROOT_DIR / "sample_data"
PDF_DIR = SAMPLE_DIR / "pdfs"
IMG_DIR = SAMPLE_DIR / "images"
TEST_DATA_DIR = ROOT_DIR / "test data"


def create_header(canvas, doc):
    canvas.saveState()
    canvas.restoreState()


def generate_cbc_pdf(filename: Path):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_CENTER
    )
    section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )
    cell_regular = ParagraphStyle(
        'CellReg',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#334155')
    )
    cell_high = ParagraphStyle(
        'CellHigh',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#DC2626')
    )
    cell_low = ParagraphStyle(
        'CellLow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#D97706')
    )
    cell_normal = ParagraphStyle(
        'CellNorm',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#16A34A')
    )

    story = []

    # Hospital Header
    story.append(Paragraph("METRO GENERAL HOSPITAL DIAGNOSTICS", title_style))
    story.append(Paragraph("Department of Hematology & Clinical Pathology • CLIA #14D0982311 • CAP #7192041", sub_style))
    story.append(Paragraph("450 Healthcare Boulevard, Suite 200 • Tel: (312) 555-0188 • Chicago, IL 60611", sub_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # Demographics Box
    demo_data = [
        [
            Paragraph("<b>Patient Name:</b> Priya Sharma", cell_regular),
            Paragraph("<b>MRN:</b> MRN-2026-000201", cell_regular),
            Paragraph("<b>Report ID:</b> RPT-2026-CBC-0891", cell_regular),
        ],
        [
            Paragraph("<b>Age / Sex:</b> 54 Yrs / Female", cell_regular),
            Paragraph("<b>DOB:</b> 1972-09-22", cell_regular),
            Paragraph("<b>Sample Type:</b> Whole Blood (EDTA)", cell_regular),
        ],
        [
            Paragraph("<b>Ordering Doctor:</b> Dr. ClinIQ Consultant", cell_regular),
            Paragraph("<b>Collection Date:</b> 2026-08-01 08:30", cell_regular),
            Paragraph("<b>Report Status:</b> FINAL / VERIFIED", cell_bold),
        ],
    ]
    t_demo = Table(demo_data, colWidths=[180, 180, 170])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 12))

    story.append(Paragraph("COMPLETE BLOOD COUNT (CBC) WITH DIFFERENTIAL", section_title))

    headers = [
        Paragraph("<b>Test Parameter</b>", cell_bold),
        Paragraph("<b>Result</b>", cell_bold),
        Paragraph("<b>Units</b>", cell_bold),
        Paragraph("<b>Reference Interval</b>", cell_bold),
        Paragraph("<b>Flag</b>", cell_bold),
    ]

    tests = [
        ("Hemoglobin (Hb)", "10.4", "g/dL", "12.0 - 15.5", "LOW", cell_low),
        ("Red Blood Cell Count (RBC)", "3.65", "x10^6/uL", "4.00 - 5.20", "LOW", cell_low),
        ("Hematocrit (Hct)", "31.8", "%", "36.0 - 46.0", "LOW", cell_low),
        ("Mean Corpuscular Volume (MCV)", "87.1", "fL", "80.0 - 100.0", "NORMAL", cell_normal),
        ("Mean Corpuscular Hemoglobin (MCH)", "28.5", "pg", "27.0 - 33.0", "NORMAL", cell_normal),
        ("MCHC", "32.7", "g/dL", "32.0 - 36.0", "NORMAL", cell_normal),
        ("Red Cell Distribution Width (RDW)", "14.2", "%", "11.5 - 14.5", "NORMAL", cell_normal),
        ("White Blood Cell Count (WBC)", "8.4", "x10^3/uL", "4.5 - 11.0", "NORMAL", cell_normal),
        ("Platelet Count", "185", "x10^3/uL", "150 - 450", "NORMAL", cell_normal),
        ("Neutrophils Absolute", "5.38", "x10^3/uL", "1.80 - 7.70", "NORMAL", cell_normal),
        ("Lymphocytes Absolute", "2.35", "x10^3/uL", "1.00 - 4.80", "NORMAL", cell_normal),
        ("Monocytes Absolute", "0.45", "x10^3/uL", "0.20 - 0.80", "NORMAL", cell_normal),
        ("Eosinophils Absolute", "0.18", "x10^3/uL", "0.02 - 0.50", "NORMAL", cell_normal),
        ("Basophils Absolute", "0.04", "x10^3/uL", "0.01 - 0.10", "NORMAL", cell_normal),
        ("Serum Ferritin", "18.2", "ng/mL", "20.0 - 200.0", "LOW", cell_low),
    ]

    t_rows = [headers]
    for name, res, units, ref, flag, style in tests:
        t_rows.append([
            Paragraph(name, cell_regular),
            Paragraph(res, cell_bold),
            Paragraph(units, cell_regular),
            Paragraph(ref, cell_regular),
            Paragraph(flag, style),
        ])

    t_table = Table(t_rows, colWidths=[180, 80, 80, 110, 80])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFF6FF')),
        ('LINEBELOW', (0,0), (-1,0), 1.2, colors.HexColor('#3B82F6')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 14))

    # Notes
    story.append(Paragraph("<b>Pathologist Comments & Interpretation:</b>", cell_bold))
    story.append(Paragraph(
        "Normocytic, normochromic mild anemia identified. Serum ferritin level of 18.2 ng/mL indicates depleted iron stores, likely secondary to chronic renal dysfunction or nutritional deficiency. Recommend correlation with serum iron, TIBC, and nephrology follow-up.",
        cell_regular
    ))
    story.append(Spacer(1, 14))

    # Sign-off
    sign_data = [
        [
            Paragraph("<b>Analyzing Instrument:</b> Sysmex XN-9000 Automated Hematology", cell_regular),
            Paragraph("<b>Verified By:</b> Dr. Karen O'Connor, MD (Hematopathologist)", cell_regular)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[270, 260])
    t_sign.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story)
    print(f"✓ Generated: {filename}")


def generate_cmp_pdf(filename: Path):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_CENTER
    )
    section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    cell_bold = ParagraphStyle('CellBold', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#0F172A'))
    cell_regular = ParagraphStyle('CellReg', fontName='Helvetica', fontSize=9, leading=11, textColor=colors.HexColor('#334155'))
    cell_high = ParagraphStyle('CellHigh', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#DC2626'))
    cell_low = ParagraphStyle('CellLow', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#D97706'))
    cell_normal = ParagraphStyle('CellNorm', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#16A34A'))

    story = []

    story.append(Paragraph("APEX SPECIALTY HEALTHCARE - DIAGNOSTIC LABORATORIES", title_style))
    story.append(Paragraph("Division of Clinical Biochemistry & Endocrinology • CLIA #36D2049182 • CAP #8829104", sub_style))
    story.append(Paragraph("750 University Avenue, Boston, MA 02115 • Tel: (617) 555-0144", sub_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=10))

    demo_data = [
        [
            Paragraph("<b>Patient Name:</b> Elena Rostova", cell_regular),
            Paragraph("<b>Patient ID:</b> PAT-00001", cell_regular),
            Paragraph("<b>Report No:</b> RPT-2026-01982", cell_regular),
        ],
        [
            Paragraph("<b>Age / Sex:</b> 52 Yrs / Female", cell_regular),
            Paragraph("<b>BMI:</b> 28.8 kg/m² (Overweight)", cell_regular),
            Paragraph("<b>Sample Type:</b> Venous Serum", cell_regular),
        ],
        [
            Paragraph("<b>Ordering Physician:</b> Dr. Arthur Vance, MD", cell_regular),
            Paragraph("<b>Collection Date:</b> 2026-03-15 07:15", cell_regular),
            Paragraph("<b>Validation Status:</b> FINAL / VERIFIED", cell_bold),
        ],
    ]
    t_demo = Table(demo_data, colWidths=[180, 180, 170])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 12))

    story.append(Paragraph("COMPREHENSIVE METABOLIC, LIPID & RENAL PANEL", section_title))

    headers = [
        Paragraph("<b>Test Parameter</b>", cell_bold),
        Paragraph("<b>Result</b>", cell_bold),
        Paragraph("<b>Units</b>", cell_bold),
        Paragraph("<b>Reference Range</b>", cell_bold),
        Paragraph("<b>Flag</b>", cell_bold),
    ]

    tests = [
        ("Fasting Blood Glucose", "164", "mg/dL", "70 - 99", "HIGH", cell_high),
        ("Glycosylated Hemoglobin (HbA1c)", "8.2", "%", "4.0 - 5.6", "HIGH", cell_high),
        ("Blood Urea Nitrogen (BUN)", "26.4", "mg/dL", "7.0 - 20.0", "HIGH", cell_high),
        ("Serum Creatinine", "1.38", "mg/dL", "0.59 - 1.04", "HIGH", cell_high),
        ("eGFR (CKD-EPI 2021)", "51", "mL/min/1.73m²", "> 60", "LOW", cell_low),
        ("Serum Sodium", "139", "mmol/L", "136 - 145", "NORMAL", cell_normal),
        ("Serum Potassium", "4.8", "mmol/L", "3.5 - 5.1", "NORMAL", cell_normal),
        ("Serum Chloride", "102", "mmol/L", "98 - 107", "NORMAL", cell_normal),
        ("Carbon Dioxide (Bicarbonate)", "24", "mmol/L", "22 - 29", "NORMAL", cell_normal),
        ("Serum Calcium", "9.4", "mg/dL", "8.6 - 10.2", "NORMAL", cell_normal),
        ("Total Cholesterol", "242", "mg/dL", "125 - 200", "HIGH", cell_high),
        ("Triglycerides", "215", "mg/dL", "< 150", "HIGH", cell_high),
        ("HDL Cholesterol", "38", "mg/dL", "> 50", "LOW", cell_low),
        ("LDL Cholesterol (Calculated)", "161", "mg/dL", "< 100", "HIGH", cell_high),
        ("Alanine Aminotransferase (ALT)", "38", "U/L", "7 - 56", "NORMAL", cell_normal),
        ("Aspartate Aminotransferase (AST)", "32", "U/L", "10 - 40", "NORMAL", cell_normal),
        ("Total Bilirubin", "0.8", "mg/dL", "0.2 - 1.2", "NORMAL", cell_normal),
        ("Serum Albumin", "4.1", "g/dL", "3.5 - 5.0", "NORMAL", cell_normal),
    ]

    t_rows = [headers]
    for name, res, units, ref, flag, style in tests:
        t_rows.append([
            Paragraph(name, cell_regular),
            Paragraph(res, cell_bold),
            Paragraph(units, cell_regular),
            Paragraph(ref, cell_regular),
            Paragraph(flag, style),
        ])

    t_table = Table(t_rows, colWidths=[180, 80, 80, 110, 80])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F9FF')),
        ('LINEBELOW', (0,0), (-1,0), 1.2, colors.HexColor('#0284C7')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Clinical Impression:</b>", cell_bold))
    story.append(Paragraph(
        "1. Uncontrolled Type 2 Diabetes Mellitus with elevated HbA1c (8.2%) and fasting hyperglycemia.<br/>"
        "2. Mixed dyslipidemia characterized by elevated total cholesterol, hypertriglyceridemia, and depressed HDL.<br/>"
        "3. Early Stage 3a Chronic Kidney Disease (eGFR 51 mL/min/1.73m²) with elevated serum creatinine (1.38 mg/dL).",
        cell_regular
    ))
    story.append(Spacer(1, 14))

    sign_data = [
        [
            Paragraph("<b>Automated System:</b> Roche Cobas 8000 c702 Analyzer", cell_regular),
            Paragraph("<b>Attending Pathologist:</b> Dr. Karen O'Connor, MD", cell_regular)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[270, 260])
    t_sign.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story)
    print(f"✓ Generated: {filename}")


def generate_clinical_note_pdf(filename: Path):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor('#0F172A'), alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#64748B'), alignment=TA_CENTER
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#1E3A8A'), spaceBefore=8, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1E293B')
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1E293B'), leftIndent=12
    )

    story = []

    story.append(Paragraph("BOSTON HEART &amp; VASCULAR INSTITUTE", title_style))
    story.append(Paragraph("Department of Cardiovascular Medicine • Outpatient Consultation Note", sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=10))

    demo_data = [
        [Paragraph("<b>Patient:</b> Arjun Mehta", body_style), Paragraph("<b>MRN:</b> MRN-2026-000101", body_style), Paragraph("<b>Date:</b> 2026-08-08", body_style)],
        [Paragraph("<b>Age/Gender:</b> 45 Yrs / Male", body_style), Paragraph("<b>Consultant:</b> Dr. ClinIQ Consultant", body_style), Paragraph("<b>Encounter:</b> Annual Review", body_style)],
    ]
    t_demo = Table(demo_data, colWidths=[180, 180, 160])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 10))

    story.append(Paragraph("SUBJECTIVE / CHIEF COMPLAINT", h2_style))
    story.append(Paragraph(
        "Patient presents for routine annual cardiovascular and general wellness examination. Reports excellent exercise tolerance, walking 5 km daily without exertional angina, orthopnea, or palpitations. Denies paroxysmal nocturnal dyspnea, lower extremity edema, or syncope.",
        body_style
    ))

    story.append(Paragraph("CURRENT MEDICATIONS", h2_style))
    story.append(Paragraph("• Multivitamin Daily — 1 tablet PO once daily with breakfast", bullet_style))
    story.append(Paragraph("• Omega-3 Fish Oil 1000mg — 1 capsule PO once daily with food", bullet_style))
    story.append(Paragraph("• Vitamin D3 1000IU — 1 capsule PO once daily (seasonal)", bullet_style))

    story.append(Paragraph("PHYSICAL EXAMINATION &amp; VITALS", h2_style))
    vitals_data = [
        [Paragraph("<b>BP:</b> 120/76 mmHg", body_style), Paragraph("<b>HR:</b> 72 bpm (Regular)", body_style), Paragraph("<b>SpO2:</b> 99% Room Air", body_style), Paragraph("<b>BMI:</b> 24.0 kg/m²", body_style)]
    ]
    t_vit = Table(vitals_data, colWidths=[130, 130, 130, 130])
    t_vit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_vit)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "General: Alert, oriented, in no acute distress. Normocephalic, atraumatic.<br/>"
        "Cardiovascular: Regular rate and rhythm, normal S1 and S2. No murmurs, gallops, or rubs. Peripheral pulses 2+ symmetric.<br/>"
        "Pulmonary: Clear to auscultation bilaterally. No wheezes, rales, or rhonchi.<br/>"
        "Abdomen: Soft, non-tender, non-distended. Normal bowel sounds. No organomegaly.",
        body_style
    ))

    story.append(Paragraph("DIAGNOSTIC DATA &amp; 5-YEAR LONGITUDINAL TREND", h2_style))
    story.append(Paragraph(
        "Longitudinal metabolic tracking from 2021 to 2026 demonstrates consistent glycemic stability (HbA1c steady at 5.2 - 5.4%), normal renal clearance (eGFR consistently &gt; 99 mL/min/1.73m², creatinine 0.88 - 0.91 mg/dL), and optimal liver transaminases. 12-lead ECG confirms normal sinus rhythm at 72 bpm with normal axis and intervals.",
        body_style
    ))

    story.append(Paragraph("ASSESSMENT &amp; PLAN", h2_style))
    story.append(Paragraph("1. <b>Cardiovascular Health:</b> Excellent. Low 10-year ASCVD risk score (&lt; 2.5%). Continue current lifestyle modifications.", bullet_style))
    story.append(Paragraph("2. <b>Preventive Care:</b> Continue daily multivitamin and omega-3 supplementation. Routine screening colonoscopy (2023) was clear; next due in 2033.", bullet_style))
    story.append(Paragraph("3. <b>Follow-Up:</b> Return in 12 months for annual comprehensive health check, or sooner PRN.", bullet_style))

    story.append(Spacer(1, 16))
    sign_data = [
        [
            Paragraph("<b>Electronically Signed:</b> Dr. ClinIQ Consultant, MD, FACC", body_style),
            Paragraph("<b>Timestamp:</b> 2026-08-08 11:45 EST", body_style)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[300, 220])
    t_sign.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story)
    print(f"✓ Generated: {filename}")


def generate_discharge_summary_pdf(filename: Path):
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor('#0F172A'), alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#64748B'), alignment=TA_CENTER
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#991B1B'), spaceBefore=8, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1E293B')
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1E293B'), leftIndent=12
    )

    story = []

    story.append(Paragraph("ST. JUDE METROPOLITAN HOSPITAL", title_style))
    story.append(Paragraph("Department of Inpatient Internal Medicine • Clinical Discharge Summary", sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#DC2626'), spaceAfter=10))

    demo_data = [
        [Paragraph("<b>Patient:</b> Priya Sharma", body_style), Paragraph("<b>MRN:</b> MRN-2026-000201", body_style), Paragraph("<b>Admission:</b> 2026-03-10", body_style)],
        [Paragraph("<b>Age/Sex:</b> 54 Yrs / Female", body_style), Paragraph("<b>Attending:</b> Dr. ClinIQ Consultant", body_style), Paragraph("<b>Discharge:</b> 2026-03-14", body_style)],
    ]
    t_demo = Table(demo_data, colWidths=[180, 180, 160])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FECACA')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 8))

    story.append(Paragraph("ADMISSION DIAGNOSIS &amp; REASON FOR HOSPITALIZATION", h2_style))
    story.append(Paragraph(
        "Hypertensive urgency with Stage 3 Chronic Kidney Disease exacerbation and symptomatic hyperglycemia (Blood Glucose 284 mg/dL, BP 178/102 mmHg, Serum Creatinine 2.1 mg/dL, eGFR 27 mL/min/1.73m²). Patient presented with headache, bilateral pedal edema, and blurred vision.",
        body_style
    ))

    story.append(Paragraph("HOSPITAL COURSE &amp; INTERVENTIONS", h2_style))
    story.append(Paragraph(
        "Patient was admitted to the intermediate medical step-down unit. Antihypertensive therapy was initiated with oral amlodipine and uptitration of lisinopril under careful telemetry and daily renal monitoring. Glycemic control was stabilized using subcutaneous basal-bolus insulin sliding scale, transitioning to oral metformin upon renal clearance verification. Serial renal panels demonstrated improvement of serum creatinine from 2.1 mg/dL to 1.55 mg/dL with resolution of acute fluid retention. Bilateral lower extremity ultrasound ruled out deep vein thrombosis.",
        body_style
    ))

    story.append(Paragraph("DISCHARGE VITALS &amp; LAB VALUES", h2_style))
    v_data = [
        [Paragraph("<b>BP:</b> 132/82 mmHg", body_style), Paragraph("<b>HR:</b> 74 bpm", body_style), Paragraph("<b>Creatinine:</b> 1.55 mg/dL", body_style), Paragraph("<b>Glucose:</b> 134 mg/dL", body_style)]
    ]
    t_v = Table(v_data, colWidths=[130, 130, 130, 130])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_v)
    story.append(Spacer(1, 6))

    story.append(Paragraph("DISCHARGE MEDICATIONS", h2_style))
    story.append(Paragraph("• Metformin 500mg — 1 tablet PO twice daily with meals", bullet_style))
    story.append(Paragraph("• Lisinopril 10mg — 1 tablet PO once daily each morning", bullet_style))
    story.append(Paragraph("• Amlodipine 5mg — 1 tablet PO once daily each evening", bullet_style))
    story.append(Paragraph("• Atorvastatin 20mg — 1 tablet PO once daily at bedtime", bullet_style))

    story.append(Paragraph("FOLLOW-UP INSTRUCTIONS &amp; RED FLAGS", h2_style))
    story.append(Paragraph(
        "1. Outpatient follow-up with Dr. ClinIQ Consultant in 7 to 10 days for repeat renal panel and blood pressure check.<br/>"
        "2. Strict low-sodium, renal-diabetic diet (sodium &lt; 2000 mg/day).<br/>"
        "3. Emergency Precautions: Present immediately to emergency department if experiencing chest pressure, severe shortness of breath, sudden visual changes, or systolic blood pressure &gt; 170 mmHg.",
        body_style
    ))

    story.append(Spacer(1, 14))
    sign_data = [
        [
            Paragraph("<b>Discharging Physician:</b> Dr. ClinIQ Consultant, MD", body_style),
            Paragraph("<b>Discharge Date:</b> 2026-03-14 14:00 EST", body_style)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[300, 220])
    t_sign.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story)
    print(f"✓ Generated: {filename}")


def copy_sample_images():
    """Copy sample medical images from test data/ into sample_data/images/ with clear clinical names."""
    if not TEST_DATA_DIR.exists():
        print(f"Warning: {TEST_DATA_DIR} does not exist.")
        return

    image_mappings = {
        "Gemini_Generated_Image_ksbs1nksbs1nksbs.png": "Lab_Report_Scan_Hematology_CBC.png",
        "Gemini_Generated_Image_qr15ptqr15ptqr15.png": "Diagnostic_Chemistry_Panel_Scan.png",
        "Screenshot 2026-07-31 193248.png": "Digital_Medical_Report_Screen.png",
        "WhatsApp Image 2026-07-31 at 11.36.44 PM.jpeg": "Clinical_Prescription_Slip_Rx.jpeg",
        "WhatsApp Image 2026-07-31 at 11.36.45 PM.jpeg": "Hospital_Vitals_Summary_Sheet.jpeg",
        "WhatsApp Image 2026-08-08 at 11.32.37 AM.jpeg": "Patient_Outpatient_Prescription.jpeg",
    }

    for src_name, dst_name in image_mappings.items():
        src_path = TEST_DATA_DIR / src_name
        dst_path = IMG_DIR / dst_name
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"✓ Copied Image: {dst_name} ({dst_path.stat().st_size // 1024} KB)")


def write_sample_data_readme():
    readme_path = SAMPLE_DIR / "README.md"
    content = """# ClinIQ Sample Clinical Test Data

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
curl -X POST "http://localhost:8056/api/v1/ingestion/patients/{patient_id}/upload" \\
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \\
  -F "file=@sample_data/pdfs/Complete_Blood_Count_CBC_Report.pdf"
```
Or open interactive API docs at `http://127.0.0.1:8056/docs`.
"""
    readme_path.write_text(content.strip(), encoding="utf-8")
    print(f"✓ Generated: {readme_path}")


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Generating ClinIQ Sample Data Repository ===")
    generate_cbc_pdf(PDF_DIR / "Complete_Blood_Count_CBC_Report.pdf")
    generate_cmp_pdf(PDF_DIR / "Comprehensive_Metabolic_Panel_CMP.pdf")
    generate_clinical_note_pdf(PDF_DIR / "Cardiology_Clinical_Consultation_Note.pdf")
    generate_discharge_summary_pdf(PDF_DIR / "Discharge_Summary_Hospital_Stay.pdf")

    copy_sample_images()
    write_sample_data_readme()

    print("=== Sample Data Generation Complete ===")


if __name__ == "__main__":
    main()
