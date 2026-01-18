import pandas as pd
import os
from data_governance.quality import check_quality
from data_governance.bias import detect_bias
from data_governance.privacy import scan_dataframe_for_pii, anonymize_text
from data_governance.lineage import emit_lineage_start, emit_lineage_complete

def main():
    print("=== 1. Generating Synthetic Data ===")
    data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "name": ["John Doe", "Jane Smith", "Alice Jones", "Bob Brown", "Charlie Davis", "Eve Wilson", "Frank Miller", "Grace Taylor", "Henry Anderson", "Ivy Thomas"],
        "gender": ["Male", "Female", "Female", "Male", "Male", "Female", "Male", "Female", "Male", "Female"],
        "income": [50000, 60000, 55000, 70000, 45000, 65000, 48000, 72000, 52000, 58000],
        "loan_approved": [1, 1, 0, 1, 0, 1, 0, 1, 0, 0], # Target
        "notes": ["Call me at 555-0101", "Email: jane@example.com", "No notes", "N/A", "Address: 123 Main St", "Confidential", "None", "See attached", "N/A", "Call 555-0199"]
    }
    # Introduce a null value
    data["income"][4] = None
    
    df = pd.DataFrame(data)
    csv_path = "test_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")

    print("\n=== 2. Testing Data Quality (Great Expectations) ===")
    quality_res = check_quality(df)
    print(f"Success: {quality_res.get('success')}")
    print(f"Statistics: {quality_res.get('statistics')}")

    print("\n=== 3. Testing Bias Detection (Fairlearn) ===")
    # Check bias in 'loan_approved' with respect to 'gender'
    bias_res = detect_bias(df, sensitive_column="gender", target_column="loan_approved")
    print("Bias Report:")
    print(bias_res)

    print("\n=== 4. Testing Privacy Controls (Presidio) ===")
    pii_report = scan_dataframe_for_pii(df)
    print(f"PII Detected in DataFrame: {pii_report}")
    
    sample_text = "My name is John and my number is 555-1234."
    anon_text = anonymize_text(sample_text)
    print(f"Anonymization Test:\nOriginal: {sample_text}\nAnonymized: {anon_text}")

    print("\n=== 5. Testing Lineage (OpenLineage) ===")
    run_id = emit_lineage_start("demo_job")
    print(f"Emitted Lineage Start Event: {run_id}")
    emit_lineage_complete(run_id, "demo_job")
    print("Emitted Lineage Complete Event")

if __name__ == "__main__":
    main()
