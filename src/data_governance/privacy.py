from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import pandas as pd
from typing import List, Dict, Any

# Initialize engines once (loading model takes time)
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def scan_text(text: str, language: str = "en") -> List[Dict[str, Any]]:
    """
    Scans text for PII using Presidio.
    """
    results = analyzer.analyze(text=text, language=language)
    return [
        {
            "type": res.entity_type,
            "start": res.start,
            "end": res.end,
            "score": res.score
        }
        for res in results
    ]

def anonymize_text(text: str, language: str = "en") -> str:
    """
    Anonymizes PII in text using Presidio (Redaction/Replacement).
    """
    results = analyzer.analyze(text=text, language=language)
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "DEFAULT": OperatorConfig("replace", {"new_value": "<PII>"})
        }
    )
    return anonymized_result.text

def scan_dataframe_for_pii(df: pd.DataFrame, sample_rows: int = 5) -> Dict[str, List[str]]:
    """
    Scans a DataFrame for PII by sampling rows.
    Returns a dictionary mapping column names to detected PII types.
    """
    pii_report = {}
    
    # Only scan object (string) columns
    string_cols = df.select_dtypes(include=['object']).columns
    
    for col in string_cols:
        detected_types = set()
        # Check sample rows
        sample_data = df[col].dropna().head(sample_rows).astype(str).tolist()
        for text in sample_data:
            results = scan_text(text)
            for res in results:
                detected_types.add(res['type'])
        
        if detected_types:
            pii_report[col] = list(detected_types)
            
    return pii_report
