import os
from datetime import datetime
from scanner import scan_accessibility
from analyzer import analyze_risk_with_gemini


class AccessibilityAgent:
    """
    高风险AI无障碍合规审计 Agent
    """

    def __init__(self):
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def run_audit(self, url):
        print(f"🚀 AccessibilityAgent: Analyzing {url}...")

        # 1. 扫描
        violations = scan_accessibility(url)

        # 2. 分析
        risk_report = analyze_risk_with_gemini(violations, url)

        # 3. 保存
        report_path = self._save_report(url, risk_report)
        return risk_report, report_path

    def _save_report(self, url, content):
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/audit_{domain}_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename


# 方便本地测试用的入口
if __name__ == "__main__":
    agent = AccessibilityAgent()
    agent.run_audit("https://www.google.com")
