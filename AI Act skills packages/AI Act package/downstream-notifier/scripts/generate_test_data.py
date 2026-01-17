#!/usr/bin/env python3
"""
Generate test data for Downstream Notifier skill.
Creates sample Excel files for Annex XII and Article 13, and sets up a mock git repo.
"""

import os
import json
import pandas as pd
from pathlib import Path
import subprocess

def create_sample_registry(base_dir):
    """Create a JSON registry of downstream providers."""
    providers = [
        {"id": "P001", "name": "Alpha Tech Solutions", "email": "contact@alphatech.example"},
        {"id": "P002", "name": "Beta Global Systems", "email": "info@betaglobal.example"},
        {"id": "P003", "name": "Gamma AI Services", "email": "admin@gammaai.example"}
    ]
    registry_path = base_dir / "test_providers.json"
    with open(registry_path, 'w') as f:
        json.dump(providers, f, indent=4)
    print(f"✓ Created {registry_path} with 3 providers.")
    return registry_path

def setup_mock_git_repo(repo_dir):
    """Initialize a git repo and make some changes to generate a diff."""
    print(f"Setting up mock git repo in {repo_dir}...")
    
    os.chdir(repo_dir)
    try:
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True, capture_output=True)
        
        # Initial commit
        file_path = repo_dir / "system_core.py"
        file_path.write_text("# Initial system core\ndef process():\n    pass\n", encoding='utf-8')
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "AI Tester"], check=True)
        # Try to commit, but ignore failed if nothing to commit
        subprocess.run(["git", "commit", "-m", "Initial commit"], capture_output=True)
        
        # Change for diff (add a special character to test encoding)
        file_path.write_text("# Updated system core\ndef process():\n    print('Now processing with filters •')\n", encoding='utf-8')
        print("✓ Mock git repo ready with pending changes (UTF-8 diff available).")
        
    except Exception as e:
        print(f"⚠ Git setup failed: {e}")

def main():
    base_dir = Path(__file__).resolve().parent.parent
    tests_dir = base_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    create_sample_registry(tests_dir)
    
    # Create a temp directory for git diff testing
    mock_repo_dir = tests_dir / "mock_repo"
    mock_repo_dir.mkdir(exist_ok=True)
    setup_mock_git_repo(mock_repo_dir)

if __name__ == "__main__":
    main()
