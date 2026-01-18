
import os
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Custom styles
        self.styles.add(ParagraphStyle(name='RiskHigh', parent=self.styles['Normal'], textColor=colors.red, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='RiskMedium', parent=self.styles['Normal'], textColor=colors.orange, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='RiskLow', parent=self.styles['Normal'], textColor=colors.green, fontName='Helvetica-Bold'))

    def _get_risk_style(self, status: str):
        if status == "HIGH": return self.styles['RiskHigh']
        if status == "MEDIUM": return self.styles['RiskMedium']
        return self.styles['RiskLow']

    def generate_pdf(self, data: Dict[str, Any], output_path: str = "conformity_report.pdf") -> str:
        """
        Generates a PDF report using ReportLab.
        """
        # Metadata
        data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "system_id" not in data: data["system_id"] = "SYS-001"

        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []

        # 1. Header
        elements.append(Paragraph("EU AI Act Conformity Assessment Report", self.styles['Title']))
        elements.append(Paragraph(f"<b>System ID:</b> {data['system_id']} | <b>Date:</b> {data['date']}", self.styles['Normal']))
        elements.append(Spacer(1, 20))

        # 2. Executive Summary
        elements.append(Paragraph("1. Executive Summary", self.styles['Heading2']))
        
        # Determine overall compliance
        risks = 0
        if data.get("quality_status") != "LOW": risks += 1
        if data.get("privacy_status") != "LOW": risks += 1
        if data.get("bias_status") != "LOW": risks += 1
        overall_status = "COMPLIANT" if risks == 0 else "NON-COMPLIANT"
        overall_color = colors.green if overall_status == "COMPLIANT" else colors.red
        
        elements.append(Paragraph(f"Overall Status: <b>{overall_status}</b>", 
                                ParagraphStyle(name='Overall', parent=self.styles['Normal'], textColor=overall_color, fontSize=14)))
        elements.append(Spacer(1, 10))

        # Summary Table
        summary_data = [
            ["Assessment Area", "Status", "Summary"],
            ["Data Quality", data.get("quality_status", "N/A"), data.get("quality_summary", "")],
            ["Privacy (GDPR)", data.get("privacy_status", "N/A"), data.get("privacy_summary", "")],
            ["Bias & Fairness", data.get("bias_status", "N/A"), data.get("bias_summary", "")],
        ]
        
        t = Table(summary_data, colWidths=[100, 80, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        # Dynamic cell coloring for risk status
        for i, key in enumerate(["quality_status", "privacy_status", "bias_status"], start=1):
            status = data.get(key, "LOW")
            bg_color = colors.green
            if status == "HIGH": bg_color = colors.red
            elif status == "MEDIUM": bg_color = colors.orange
            
            t.setStyle(TableStyle([('TEXTCOLOR', (1, i), (1, i), bg_color), ('FONTNAME', (1, i), (1, i), 'Helvetica-Bold')]))

        elements.append(t)
        elements.append(Spacer(1, 20))

        # 3. Detailed Analysis
        elements.append(Paragraph("2. Detailed Risk Analysis", self.styles['Heading2']))
        
        # Privacy
        elements.append(Paragraph("2.1 Privacy & Data Protection", self.styles['Heading3']))
        privacy_risks = data.get("privacy_risks", [])
        if privacy_risks:
            for risk in privacy_risks:
                elements.append(Paragraph(f"• <b>{risk.get('column', 'Unknown')}</b>: {risk.get('type', 'Unknown Risk')}", self.styles['Normal']))
        else:
            elements.append(Paragraph("No PII detected.", self.styles['Normal']))
            
        elements.append(Spacer(1, 10))

        # Bias
        elements.append(Paragraph("2.2 Bias & Fairness", self.styles['Heading3']))
        elements.append(Paragraph(f"Details: {data.get('bias_details', 'N/A')}", self.styles['Normal']))
        elements.append(Spacer(1, 10))

        # Environment
        elements.append(Paragraph("3. Environmental Impact", self.styles['Heading2']))
        elements.append(Paragraph(f"Estimated Carbon Footprint: <b>{data.get('carbon_footprint', '0')} kgCO2</b>", self.styles['Normal']))

        # Build PDF
        doc.build(elements)
        return os.path.abspath(output_path)

def generate_compliance_report(analysis_results: Dict[str, Any]) -> str:
    generator = ReportGenerator()
    return generator.generate_pdf(analysis_results)
