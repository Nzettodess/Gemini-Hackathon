"""
Fake Annex XII Data Generator for Testing.
Simulates user-provided GPAI model information.
"""
import json
from pathlib import Path
from datetime import datetime

def generate_fake_annex_xii(provider_name="Test AI Corp", model_name="GPT-X"):
    """Generate fake Annex XII (GPAI) input data for testing."""
    
    return {
        # Provider Information
        "provider_name": provider_name,
        "provider_id": f"GPAI-{datetime.now().strftime('%Y%m%d')}",
        "contact_email": f"compliance@{provider_name.lower().replace(' ', '')}.com",
        "contact_phone": "+1-555-0123",
        "address": "123 AI Boulevard, Tech City, TC 12345",
        
        # Model Information
        "model_name": model_name,
        "model_version": "v2.1.0",
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        
        # XII.1.a - Intended Tasks
        "intended_tasks": f"{model_name} is designed for natural language understanding, text generation, and multi-turn conversation. It can be integrated into customer service platforms, content creation tools, and research assistants.",
        
        # XII.1.b - Acceptable Use / Prohibited Uses
        "acceptable_use": "Business communication, content drafting, code assistance, educational support.",
        "prohibited_uses": "Generating harmful content, impersonation, automated decision-making affecting legal rights, surveillance applications.",
        
        # XII.1.c - Distribution
        "distribution_methods": "API access, SDK integration, cloud deployment.",
        
        # XII.1.d - Hardware/Software Interaction
        "hardware_requirements": "Minimum 16GB RAM, NVIDIA GPU recommended for local inference. Cloud deployment available.",
        "api_specifications": "RESTful API with JSON request/response. WebSocket support for streaming.",
        
        # XII.1.e - Software Dependencies
        "software_versions": "Python 3.10+, PyTorch 2.0+, transformers 4.30+",
        "dependencies": "CUDA 11.8+ for GPU acceleration, Docker for containerized deployment.",
        
        # XII.1.f - Architecture
        "architecture": "Transformer-based decoder-only architecture with 7B parameters. 32 attention layers, 4096 hidden dimension.",
        "parameter_count": "7 billion parameters",
        
        # XII.1.g - Modalities
        "input_modality": "Text (UTF-8 encoded), maximum context length 8192 tokens.",
        "output_modality": "Text generation, structured JSON output, code generation.",
        
        # XII.1.h - License
        "license": "Commercial license with usage-based pricing. Research use permitted under academic agreement.",
        
        # XII.2.a - Integration
        "integration_instructions": "1. Obtain API key from developer portal. 2. Install SDK: pip install gpai-client. 3. Initialize client with credentials. 4. Send requests via API.",
        "infrastructure_requirements": "Minimum 100Mbps network connection. Load balancer recommended for production.",
        
        # XII.2.b - Context/Limits
        "context_window": "8192 tokens",
        "rate_limits": "100 requests/minute on standard tier, 1000 requests/minute on enterprise tier.",
        
        # XII.2.c - Training Data
        "training_data_type": "Web crawl data, curated text corpora, licensed content partnerships.",
        "data_provenance": "Data sourced from publicly available web content (pre-2024), filtered for quality and safety.",
        
        # Checklist status (all should be "Yes" for a complete model)
        "checklist": {
            "XII_1_a": "Yes",
            "XII_1_b": "Yes", 
            "XII_1_c": "Yes",
            "XII_1_d": "Yes",
            "XII_1_e": "Yes",
            "XII_1_f": "Yes",
            "XII_1_g": "Yes",
            "XII_1_h": "Yes",
            "XII_2_a": "Yes",
            "XII_2_b": "Yes",
            "XII_2_c": "Yes",
            "Art_53_1_b": "Yes"
        }
    }

def save_fake_annex_xii(output_dir="examples"):
    """Generate and save fake Annex XII data for multiple test providers."""
    
    providers = [
        ("Zenith AI Systems", "ZenithGPT-4"),
        ("Alpha Medical AI", "MedAssist-Pro"),
        ("Beta Financial Tech", "FinanceBot-X"),
        ("Gamma Logistics AI", "LogiPredict-3")
    ]
    
    Path(output_dir).mkdir(exist_ok=True)
    
    for provider_name, model_name in providers:
        data = generate_fake_annex_xii(provider_name, model_name)
        filename = f"{provider_name.replace(' ', '_')}_AnnexXII.json"
        filepath = Path(output_dir) / filename
        filepath.write_text(json.dumps(data, indent=2))
        print(f"Created: {filepath}")
    
    return True

if __name__ == "__main__":
    save_fake_annex_xii()
