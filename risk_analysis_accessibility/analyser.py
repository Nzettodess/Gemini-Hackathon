import ssl

# 忽略 SSL 证书验证
ssl._create_default_https_context = ssl._create_unverified_context

import google.generativeai as genai
import json

# 使用群公告里的 Key
API_KEY = "AIzaSyCE80aDphpFlSv_3nM3nbyS-kVPESEDZHw"
genai.configure(api_key=API_KEY)


def analyze_risk_with_gemini(scan_results, target_url):
    """
    调用 Gemini 2.5 Flash 分析无障碍扫描结果的法律风险
    """
    print(f"[*] Sending {len(scan_results)} violations to Gemini for legal analysis...")

    if not scan_results:
        return "No technical violations found. The system appears compliant with WCAG 2.1 Level AA."

    try:
        # --- 修改点：使用列表中确认存在的 gemini-2.5-flash ---
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 构造提示词
        prompt = f"""
        You are an EU AI Act Compliance Officer specializing in Fundamental Rights.

        Target System: {target_url}
        Context: We performed an automated accessibility scan (WCAG standard).

        Technical Violations Found (JSON):
        {json.dumps(scan_results)}

        Task:
        Based on the technical violations above, generate a Risk Analysis Report regarding **Fundamental Rights (Article 27 / EU Charter Art 26)**.

        Please structure your response as follows:
        1. **Executive Summary**: Is this system compliant? (Yes/No/Partial)
        2. **Human Rights Impact**: Specifically, how do these errors discriminate against disabled users?
        3. **Legal Risk Assessment**: High/Medium/Low risk under the EU AI Act.
        4. **Remediation Plan**: 3 key technical steps to fix the issues.

        Keep the tone professional and strict.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"[!] AI Analysis Failed. Error details: {str(e)}"


# 测试代码
if __name__ == "__main__":
    mock_data = [{"impact": "critical", "description": "ARIA attributes must conform to valid values"}]
    print(analyze_risk_with_gemini(mock_data, "test.com"))
