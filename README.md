# CorpShield AI 🛡️
### Corporate Financial Statement Anomaly Surveillance & Fraud Screening System

CorpShield AI is an AI-powered corporate financial statement anomaly detection and forensic screening prototype designed for academic and student research, aligned with the investor-protection surveillance objectives of regulators such as SEBI.

---

## 🏛️ Surveillance Architecture & Key Capabilities

1. **Unsupervised Outlier Detection (Isolation Forest)**:
   - Evaluates multi-dimensional financial ratios without requiring historical fraud labels.
   - Detects statistical anomalies and uncharacteristic corporate balance-sheet distortions.
   - Generates normalized anomaly scores ($0-100$) and outlier flags.

2. **Supervised Pattern Classification (Random Forest)**:
   - Evaluates non-linear combinations of engineered forensic ratios against simulated anomaly cohorts.
   - Uses strict **Group-Wise Validation (`GroupShuffleSplit`)** on company identifiers to prevent temporal and entity data leakage across financial reporting periods.
   - Extracts feature importance rankings showing the primary drivers of model decisions (e.g. Sloan's Accrual Ratio, Operating Cash Flow to Net Income, Profit Margin shifts).

3. **Explainable Forensic Warning Rules Engine**:
   - Implements 6 configurable forensic accounting heuristic rules based on classical forensic literature (Beneish M-Score, Sloan 1996):
     - **Revenue vs. Operating Cash Flow Divergence** (Quality of earnings check)
     - **Receivables Growth Outstripping Revenue** (Channel stuffing and fictitious sales check)
     - **Positive Net Income with Operating Cash Deficit** (Accrual manipulation check)
     - **High Debt Leverage & Solvency Deterioration** (Solvency distress check)
     - **Abrupt Profit Margin Anomaly** (Arbitrary cost allocation / non-recurring shift check)
     - **Material Related-Party Transactions** (Non-arm's length fund routing check)
   - Every triggered warning details: actual values, prior period baseline, forensic rationale, legitimate business explanations, and recommended audit checklist.

4. **Transparent Composite Screening Score**:
   - Calculates a multi-dimensional priority score ($0-100$):
     $$\text{Composite Score} = 0.35 \times \text{IF Score} + 0.35 \times \text{RF Likelihood} + 0.30 \times \text{Rules Score}$$
   - Classifies filings into actionable review tiers:
     - 🚨 **HIGH PRIORITY** ($\ge 65.0$ or $\ge 3$ critical rules): Urgent investigation queue.
     - ⚠️ **MODERATE PRIORITY** ($35.0 - 64.9$): Surveillance watchlist.
     - ✅ **LOW PRIORITY** ($< 35.0$): Standard baseline conformance.

5. **Futuristic Financial Surveillance Command Center**:
   - 6 Dedicated Navigation Sections:
     - **1. Command Center**: Real-time KPI tiles, interactive scatter plots, score distributions, and filterable ranked surveillance queue.
     - **2. Company Risk Analysis**: Entity deep dive, multi-period financial trajectory charts, timeline of anomaly emergence, ratio deconstruction, and auditor notes.
     - **3. Upload & Analyze**: Ingest custom CSV datasets with automatic schema and type validation, plus a Single-Company Manual Entry Terminal.
     - **4. AI Model Laboratory**: Model architecture specs, metrics (Precision, Recall, F1, ROC-AUC, PR-AUC), confusion matrix heatmap, feature importance bar chart, feature dictionary, and one-click live retraining.
     - **5. Financial Reports**: Downloadable formatted HTML intelligence dossiers (ready for printing or saving to PDF) and analyzed CSV export.
     - **6. Data Sources & Methodology**: Full mathematical scoring formulation, SEBI investor-protection principles, and academic provenance notes.

---

## 📁 Modular Project Structure

```
corpshield/
├── app.py                      # Main Streamlit financial surveillance application
├── data_loader.py              # Root alias for data ingestion & synthetic dataset generation
├── feature_engineering.py      # Root alias for forensic ratio calculations
├── model_training.py           # Root alias for model fitting & group validation
├── anomaly_detection.py        # Root alias for CorpShieldAnalyzer pipeline
├── risk_rules.py               # Root alias for heuristic forensic rules
├── report_generator.py         # Root alias for HTML dossier generation
├── pytest.ini                  # Pytest configuration
├── real_companies_data.csv     # Audited public disclosures (AAPL, MSFT, TSLA, etc.)
├── data/
│   └── synthetic_financials.csv # Reproducible research cohort (120 companies, 720 periods)
├── models/
│   ├── preprocessor_if.joblib  # Fitted preprocessing pipeline for Isolation Forest
│   ├── unsupervised_if.joblib  # Fitted Isolation Forest model
│   ├── preprocessor_rf.joblib  # Fitted preprocessing pipeline for Random Forest
│   └── supervised_rf.joblib    # Fitted Random Forest model
├── reports/
│   └── model_evaluation.json   # Machine-learning evaluation metrics and feature importances
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   ├── anomaly_detection.py
│   ├── risk_rules.py
│   ├── report_generator.py
│   ├── predict.py
│   └── train.py
└── tests/
    ├── test_validation.py      # Schema, type, negative asset, duplicate checks
    ├── test_features.py        # Ratio math, zero/negative denominator safeguards
    ├── test_risk_rules.py       # Heuristic rule triggers and explanations
    └── test_models.py          # ML analyzer inference and priority tiering
```

---

## 🧪 Automated Testing

Execute the comprehensive 14-test verification suite:

```bash
pytest
```

---

## 🚀 Running the Surveillance Application

1. **Verify or retrain models** (optional; pre-trained weights are included):
   ```bash
   python -m src.train
   ```

2. **Launch the Streamlit Surveillance Dashboard**:
   ```bash
   streamlit run app.py
   ```
   Open **http://localhost:8501** in your web browser.

---

## ⚖️ Regulatory & Academic Disclaimer

> **IMPORTANT:** CorpShield AI is a student research and educational screening prototype for corporate financial anomaly detection. 
> Its predictions, scores, and warning flags **do not establish legal proof of fraud, provide investment advice, or represent an official assessment by SEBI (Securities and Exchange Board of India)** or any regulatory agency. 
> Statistical and accounting anomalies frequently have legitimate business explanations (e.g. capital expansion cycles, seasonal cash collections, or milestone billing). All findings require independent corroboration against certified statutory filings.
