#!/usr/bin/env python3
"""
Download GitHub repositories from the provided risk tools list
into Risks packages folder following the categories logic folder.
"""

import os
import subprocess
from urllib.parse import urlparse
import json
from datetime import datetime

# Category mapping from Excel to folder names
CATEGORY_MAPPING = {
    'Legal': 'Legal',
    'Cybersecurity': 'Cybersecurity',
    'Environment': 'Environment',
    'Technical': 'Technical',
    'Trust': 'Trust',
    'Fundamental Rights': 'Fundamental Rights',
    'Privacy': 'EU AI Act Compliance',
    'Societal': 'Societal',
    'Third-Party': 'Third-Party',
    'Business': 'Societal',
    'Health & Safety': 'Health & Safety',
    'GDPR Compliance': 'EU AI Act Compliance',
    'EU AI Act Compliance': 'EU AI Act Compliance'
}

# Complete list of tools from the provided screenshot
TOOLS_LIST = [
    # Legal
    ('Legal', 'SPDX License Checker', 'https://spdx.org/licenses/'),
    ('Legal', 'TinEye Reverse Image Search', 'https://tineye.com/'),
    ('Legal', 'Copyscape Plagiarism Checker', 'https://www.copyscape.com/'),
    ('Legal', 'EUR-Lex API', 'https://eur-lex.europa.eu/api'),

    # Cybersecurity
    ('Cybersecurity', 'HaveIBeenPwned API', 'https://api.pwnedpasswords.com/'),
    ('Cybersecurity', 'NVD CVE Lookup', 'https://services.nvd.nist.gov/rest/json/cves/2.0'),
    ('Cybersecurity', 'VirusTotal API', 'https://www.virustotal.com/api/v3/'),
    ('Cybersecurity', 'Shodan Search', 'https://api.shodan.io/'),
    ('Cybersecurity', 'URLhaus Malware URLs', 'https://urlhaus-api.abuse.ch/v1/'),
    ('Cybersecurity', 'Hardenize', 'https://www.hardenize.com/'),
    ('Cybersecurity', 'SSL Labs API', 'https://api.ssllabs.com/api/v3/'),
    ('Cybersecurity', 'AbuseIPDB', 'https://api.abuseipdb.com/api/v2/'),
    ('Cybersecurity', 'Prompt Injection Detector', 'https://github.com/protectai/rebuff'),

    # Environment
    ('Environment', 'CodeCarbon', 'https://github.com/mlco2/codecarbon'),
    ('Environment', 'ML CO2 Impact Calculator', 'https://mlco2.github.io/impact/'),
    ('Environment', 'Electricity Maps API', 'https://api.electricitymap.org/'),
    ('Environment', 'Green Web Foundation API', 'https://api.thegreenwebfoundation.org/'),
    ('Environment', 'Cloud Carbon Footprint', 'https://github.com/cloud-carbon-footprint/cloud-carbon-footprint'),
    ('Environment', 'Website Carbon Calculator', 'https://api.websitecarbon.com/'),

    # Technical
    ('Technical', 'Evidently AI', 'https://github.com/evidentlyai/evidently'),
    ('Technical', 'Alibi Detect', 'https://github.com/SeldonIO/alibi-detect'),
    ('Technical', 'RAGAS', 'https://github.com/explodinggradients/ragas'),
    ('Technical', 'DeepEval', 'https://github.com/confident-ai/deepeval'),
    ('Technical', 'Hugging Face Evaluate', 'https://github.com/huggingface/evaluate'),
    ('Technical', 'LangSmith', 'https://smith.langchain.com/'),
    ('Technical', 'Weights & Biases', 'https://wandb.ai/'),
    ('Technical', 'PromptFoo', 'https://github.com/promptfoo/promptfoo'),

    # Trust
    ('Trust', 'SHAP Explainer', 'https://github.com/slundberg/shap'),
    ('Trust', 'LIME', 'https://github.com/marcotcr/lime'),
    ('Trust', 'Captum', 'https://github.com/pytorch/captum'),
    ('Trust', 'InterpretML', 'https://github.com/interpretml/interpret'),
    ('Trust', 'What-If Tool', 'https://github.com/PAIR-code/what-if-tool'),
    ('Trust', 'Axe Accessibility', 'https://github.com/dequelabs/axe-core'),

    # Fundamental Rights
    ('Fundamental Rights', 'AI Fairness 360', 'https://github.com/Trusted-AI/AIF360'),
    ('Fundamental Rights', 'Fairlearn', 'https://github.com/fairlearn/fairlearn'),
    ('Fundamental Rights', 'Aequitas', 'https://github.com/dssg/aequitas'),
    ('Fundamental Rights', 'Perspective API', 'https://perspectiveapi.com/'),
    ('Fundamental Rights', 'Moderation API', 'https://api.openai.com/v1/moderations'),
    ('Fundamental Rights', 'Disaggregated Evaluation', 'https://github.com/Trusted-AI/AIF360'),

    # Privacy
    ('Privacy', 'Presidio', 'https://github.com/microsoft/presidio'),
    ('Privacy', 'spaCy NER', 'https://github.com/explosion/spaCy'),
    ('Privacy', 'Faker', 'https://github.com/joke2k/faker'),
    ('Privacy', 'ARX Data Anonymization', 'https://github.com/arx-deidentifier/arx'),
    ('Privacy', 'OpenDP', 'https://github.com/opendp/opendp'),
    ('Privacy', 'Email Validator', 'https://hunter.io/'),

    # Societal
    ('Societal', 'Perspective API', 'https://perspectiveapi.com/'),
    ('Societal', 'Detoxify', 'https://github.com/unitaryai/detoxify'),
    ('Societal', 'ClaimBuster API', 'https://idir.uta.edu/claimbuster/api/'),
    ('Societal', 'TextBlob Sentiment', 'https://github.com/sloria/TextBlob'),
    ('Societal', 'VADER Sentiment', 'https://github.com/cjhutto/vaderSentiment'),
    ('Societal', 'Hate Speech Detector', 'https://github.com/Hironsan/HateSonar'),
    ('Societal', 'Misinformation Keywords', 'https://idir.uta.edu/claimbuster/'),

    # Third-Party
    ('Third-Party', 'Snyk OSS', 'https://snyk.io/'),
    ('Third-Party', 'Safety (PyUp)', 'https://github.com/pyupio/safety'),
    ('Third-Party', 'Syft SBOM Generator', 'https://github.com/anchore/syft'),
    ('Third-Party', 'Grype Vulnerability Scanner', 'https://github.com/anchore/grype'),
    ('Third-Party', 'OSSF Scorecard', 'https://github.com/ossf/scorecard'),
    ('Third-Party', 'License Checker', 'https://github.com/nexB/scancode-toolkit'),

    # Health & Safety
    ('Health & Safety', 'FHIR Validator', 'https://fhir.org/'),
    ('Health & Safety', 'ICD-10 Lookup', 'https://clinicaltables.nlm.nih.gov/api/'),
    ('Health & Safety', 'OpenFDA Drug API', 'https://api.fda.gov/drug/event.json?limit=1'),
    ('Health & Safety', 'Confidence Calibration', 'https://github.com/uncertainty-toolbox/uncertainty-toolbox'),
    ('Health & Safety', 'Critical Alert Detector', 'https://grafana.com/oss/grafana/'),

    # GDPR Compliance
    ('GDPR Compliance', 'OneTrust DPIA Tool', 'https://www.onetrust.com/products/privacy-impact-assessment/'),
    ('GDPR Compliance', 'Cookiebot Scanner', 'https://www.cookiebot.com/'),
    ('GDPR Compliance', 'GDPR Enforcement Tracker API', 'https://www.enforcementtracker.com/'),
    ('GDPR Compliance', 'DataGrail DSAR Automation', 'https://www.datagrail.io/'),
    ('GDPR Compliance', 'PrivacyPolicies.com Generator', 'https://www.privacypolicies.com/'),
    ('GDPR Compliance', 'Breach Notification Calculator', 'https://trustedpa.com/free-tools/gdpr-fine-calculator/'),
    ('GDPR Compliance', 'Lawful Basis Assessment Tool', 'https://ico.org.uk/for-organisations/lawful-basis-interactive-guidance-tool/'),
    ('GDPR Compliance', 'Record of Processing (RoPA) Tool', 'https://iapp.org/gdpr-ccpa-templates/'),
    ('GDPR Compliance', 'Transcend Data Mapping', 'https://transcend.io/'),
    ('GDPR Compliance', 'International Transfer Assessment', 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/'),

    # EU AI Act Compliance
    ('EU AI Act Compliance', 'Model Cards Generator', 'https://huggingface.co/docs/hub/model-cards'),
    ('EU AI Act Compliance', 'Conformity Assessment Checklist', 'https://verifywise.ai/'),
    ('EU AI Act Compliance', 'AI System Registry', 'https://ec.europa.eu/'),
    ('EU AI Act Compliance', 'Technical Documentation Generator', 'https://github.com/mkdocs/mkdocs'),
    ('EU AI Act Compliance', 'AI Transparency Labels', 'https://airtransparency.ai/label/'),
    ('EU AI Act Compliance', 'FRIA Generator', 'https://www.humanrights.dk/tools/human-rights-impact-assessment-guidance-toolbox'),
    ('EU AI Act Compliance', 'Post-Market Monitoring Dashboard', 'https://sourceforge.net/projects/opensourcepv/'),
    ('EU AI Act Compliance', 'Serious Incident Reporter', 'https://github.com/TheHive-Project/TheHive'),
    ('EU AI Act Compliance', 'Quality Management System (QMS) Tracker', 'https://linxio.com/'),
    ('EU AI Act Compliance', 'AI Logging System', 'https://grafana.com/oss/loki/'),
    ('EU AI Act Compliance', 'CE Marking Generator', 'https://ce-marking.help/'),
]

def is_github_url(url):
    """Check if URL is a GitHub repository URL."""
    if not url or not isinstance(url, str):
        return False
    return 'github.com' in url.lower() and url.startswith('http')

def get_repo_name(github_url):
    """Extract repository name from GitHub URL."""
    parts = github_url.rstrip('/').split('/')
    if len(parts) >= 2:
        return parts[-1]
    return None

def clone_repository(github_url, target_dir, tool_name):
    """Clone a GitHub repository to target directory."""
    repo_name = get_repo_name(github_url)
    if not repo_name:
        return False, "Could not parse repository name"

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Full path for the cloned repo
    repo_path = os.path.join(target_dir, repo_name)

    # Check if already exists
    if os.path.exists(repo_path):
        return True, f"Already exists: {repo_path}"

    # Clone the repository
    try:
        print(f"  Cloning {github_url} to {repo_path}...")
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', github_url, repo_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            return True, f"Successfully cloned to {repo_path}"
        else:
            return False, f"Git clone failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Clone timeout (5 minutes)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main function to process list and download repositories."""

    # Base paths
    base_dir = '/Users/miachen/Desktop/Mia/DT Master/Tech/Hackthon/geminihackathon'
    risks_packages_dir = os.path.join(base_dir, 'Risks packages')

    # Statistics
    stats = {
        'total_tools': len(TOOLS_LIST),
        'github_tools': 0,
        'downloaded': 0,
        'skipped': 0,
        'failed': 0,
        'already_exists': 0,
        'by_category': {}
    }

    # Detailed log
    download_log = []

    print("\nProcessing tools from provided list...\n")

    # Process each tool
    for idx, (category, tool_name, url) in enumerate(TOOLS_LIST, 1):
        # Initialize category stats
        if category not in stats['by_category']:
            stats['by_category'][category] = {
                'total': 0,
                'downloaded': 0,
                'skipped': 0,
                'failed': 0
            }

        stats['by_category'][category]['total'] += 1

        # Check if it's a GitHub URL
        if is_github_url(url):
            stats['github_tools'] += 1

            print(f"[{idx}/{len(TOOLS_LIST)}] {category} - {tool_name}")
            print(f"  URL: {url}")

            # Map category to folder
            target_folder = CATEGORY_MAPPING.get(category, category)
            target_dir = os.path.join(risks_packages_dir, target_folder)

            # Clone repository
            success, message = clone_repository(url, target_dir, tool_name)

            print(f"  {message}\n")

            log_entry = {
                'index': idx,
                'category': category,
                'tool_name': tool_name,
                'github_url': url,
                'target_folder': target_folder,
                'success': success,
                'message': message
            }
            download_log.append(log_entry)

            if success:
                if 'Already exists' in message:
                    stats['already_exists'] += 1
                    stats['by_category'][category]['skipped'] += 1
                else:
                    stats['downloaded'] += 1
                    stats['by_category'][category]['downloaded'] += 1
            else:
                stats['failed'] += 1
                stats['by_category'][category]['failed'] += 1
        else:
            print(f"[{idx}/{len(TOOLS_LIST)}] {category} - {tool_name}")
            print(f"  Skipped (Not a GitHub URL): {url}\n")
            stats['skipped'] += 1
            stats['by_category'][category]['skipped'] += 1

    # Print summary
    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"Total tools in list: {stats['total_tools']}")
    print(f"Tools with GitHub URLs: {stats['github_tools']}")
    print(f"Successfully downloaded: {stats['downloaded']}")
    print(f"Already existed: {stats['already_exists']}")
    print(f"Skipped (non-GitHub): {stats['skipped']}")
    print(f"Failed: {stats['failed']}")

    print("\n" + "-"*80)
    print("BY CATEGORY:")
    print("-"*80)
    for category, cat_stats in sorted(stats['by_category'].items()):
        print(f"\n{category}:")
        print(f"  Total: {cat_stats['total']}")
        print(f"  Downloaded: {cat_stats['downloaded']}")
        print(f"  Skipped: {cat_stats['skipped']}")
        print(f"  Failed: {cat_stats['failed']}")

    # Save detailed log
    log_file = os.path.join(risks_packages_dir, 'DOWNLOAD_LOG_COMPLETE.json')
    with open(log_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'downloads': download_log
        }, f, indent=2)

    print(f"\n\nDetailed log saved to: {log_file}")

    # Update markdown summary
    md_file = os.path.join(risks_packages_dir, 'DOWNLOAD_SUMMARY.md')
    with open(md_file, 'w') as f:
        f.write("# Risk Tools Complete Download Summary\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Statistics\n\n")
        f.write(f"- Total tools in list: {stats['total_tools']}\n")
        f.write(f"- Tools with GitHub URLs: {stats['github_tools']}\n")
        f.write(f"- Successfully downloaded (new): {stats['downloaded']}\n")
        f.write(f"- Already existed: {stats['already_exists']}\n")
        f.write(f"- Skipped (non-GitHub URLs): {stats['skipped']}\n")
        f.write(f"- Failed: {stats['failed']}\n\n")

        f.write("## By Category\n\n")
        for category, cat_stats in sorted(stats['by_category'].items()):
            target_folder = CATEGORY_MAPPING.get(category, category)
            f.write(f"### {category} → `{target_folder}`\n\n")
            f.write(f"- Total: {cat_stats['total']}\n")
            f.write(f"- Downloaded: {cat_stats['downloaded']}\n")
            f.write(f"- Skipped: {cat_stats['skipped']}\n")
            f.write(f"- Failed: {cat_stats['failed']}\n\n")

        if stats['downloaded'] > 0:
            f.write("## Newly Downloaded Tools\n\n")
            for entry in download_log:
                if entry['success'] and 'Already exists' not in entry['message']:
                    f.write(f"- **{entry['tool_name']}** ({entry['category']})\n")
                    f.write(f"  - URL: {entry['github_url']}\n")
                    f.write(f"  - Location: `Risks packages/{entry['target_folder']}/`\n\n")

        if stats['failed'] > 0:
            f.write("## Failed Downloads\n\n")
            for entry in download_log:
                if not entry['success']:
                    f.write(f"- **{entry['tool_name']}** ({entry['category']})\n")
                    f.write(f"  - URL: {entry['github_url']}\n")
                    f.write(f"  - Error: {entry['message']}\n\n")

    print(f"Markdown summary saved to: {md_file}")

if __name__ == '__main__':
    main()
