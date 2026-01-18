import pandas as pd
from mcp.server.fastmcp import FastMCP
from data_governance.quality import check_quality
from data_governance.bias import detect_bias
from data_governance.privacy import scan_dataframe_for_pii, anonymize_text
from data_governance.lineage import emit_lineage_start, emit_lineage_complete
from data_governance.environment import estimate_carbon_footprint
from data_governance.security import scan_prompt_for_risk
from data_governance.reporting import generate_compliance_report
import traceback
import json

# Initialize FastMCP server
mcp = FastMCP("Data Governance Server")

def load_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Failed to load CSV from {path}: {str(e)}")

@mcp.tool()
def check_data_quality(csv_path: str) -> str:
    """
    Checks the data quality of a CSV file using Great Expectations.
    Returns a summary of validation results.
    """
    run_id = emit_lineage_start("check_data_quality")
    try:
        df = load_csv(csv_path)
        results = check_quality(df)
        emit_lineage_complete(run_id, "check_data_quality")
        
        # Simplify output for LLM
        success = results.get("success", False)
        stats = results.get("statistics", {})
        return f"Quality Check Status: {'PASSED' if success else 'FAILED'}\nStatistics: {stats}"
    except Exception as e:
        return f"Error: {traceback.format_exc()}"

@mcp.tool()
def analyze_bias(csv_path: str, sensitive_column: str, target_column: str = None) -> str:
    """
    Analyzes bias in a CSV file using Fairlearn.
    Requires a sensitive column (e.g., gender, race).
    Optionally checks against a target column (label).
    """
    run_id = emit_lineage_start("analyze_bias")
    try:
        df = load_csv(csv_path)
        if sensitive_column not in df.columns:
            return f"Error: Column '{sensitive_column}' not found in dataset."
            
        results = detect_bias(df, sensitive_column, target_column)
        emit_lineage_complete(run_id, "analyze_bias")
        return str(results)
    except Exception as e:
        return f"Error: {traceback.format_exc()}"

@mcp.tool()
def scan_privacy(csv_path: str) -> str:
    """
    Scans a CSV file for PII (Personal Identifiable Information) using Presidio.
    Returns a report of detected PII types per column.
    """
    run_id = emit_lineage_start("scan_privacy")
    try:
        df = load_csv(csv_path)
        report = scan_dataframe_for_pii(df)
        emit_lineage_complete(run_id, "scan_privacy")
        
        if not report:
            return "No PII detected in sampled rows."
        return f"PII Detected: {report}"
    except Exception as e:
        return f"Error: {traceback.format_exc()}"

@mcp.tool()
def anonymize_content(text: str) -> str:
    """
    Anonymizes the input text by replacing PII with placeholders.
    """
    return anonymize_text(text)

@mcp.tool()
def estimate_ai_emissions(duration_seconds: float, hardware_type: str = "cpu") -> str:
    """
    Estimates the carbon footprint of an AI task based on duration and hardware.
    hardware_type: 'cpu', 'gpu_t4', 'gpu_a100'
    """
    result = estimate_carbon_footprint(duration_seconds, hardware_type)
    return f"Estimated Carbon Footprint: {result['estimated_emissions_kg']:.4f} kgCO2 (Energy: {result['estimated_energy_kwh']:.4f} kWh)"

@mcp.tool()
def scan_prompt_security(prompt: str) -> str:
    """
    Scans a prompt for security risks (Injection, Jailbreak, etc.).
    """
    result = scan_prompt_for_risk(prompt)
    if result["safe"]:
        return "✅ No security risks detected."
    
    report = "⚠️ Security Risks Detected:\n"
    for risk in result["detected_risks"]:
        report += f"- [{risk['severity']}] {risk['type']}: {risk.get('details', 'Pattern matched')}\n"
    return report

import asyncio
from concurrent.futures import ThreadPoolExecutor

# Create a thread pool for blocking operations
pool = ThreadPoolExecutor()

@mcp.tool()
async def generate_conformity_report(data_json: str) -> str:
    """
    Generates a PDF Conformity Assessment Report (EU AI Act) from analysis results.
    input: JSON string containing 'quality_summary', 'privacy_summary', etc.
    """
    try:
        data = json.loads(data_json)
        # Run the blocking PDF generation in a separate thread to avoid blocking the asyncio loop
        loop = asyncio.get_running_loop()
        pdf_path = await loop.run_in_executor(pool, generate_compliance_report, data)
        return f"✅ Report generated successfully: {pdf_path}"
    except Exception as e:
        return f"Error generating report: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
