import pandas as pd
import sys

def inspect_excel(path):
    print(f"\n{'='*20} INSPECTING: {path} {'='*20}")
    try:
        with pd.ExcelFile(path, engine='openpyxl') as xls:
            for sheet in xls.sheet_names:
                print(f"\n--- Sheet: {sheet} ---")
                df = pd.read_excel(xls, sheet_name=sheet)
                print(f"Columns: {df.columns.tolist()}")
                print(f"Shape: {df.shape}")
                print("\nHead Data (top 10 rows):")
                print(df.head(10).to_string())
    except Exception as e:
        print(f"Error inspecting {path}: {e}")

if __name__ == "__main__":
    inspect_excel('Output/EU_AI_Act_Annex_XII_Downstream_Provider_Template.xlsx')
    inspect_excel('Output/EU_AI_Act_Article_13_Compliance_Template.xlsx')
