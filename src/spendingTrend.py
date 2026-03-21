from collections import defaultdict
from datetime import datetime
import csv
import os

class SpendingTrend:
    def __init__(self):
        self.spending_data = defaultdict(lambda: defaultdict(float))

    def add_spending(self, date, category, amount):
        month = date.strftime("%Y-%m") if isinstance(date, datetime) else date
        self.spending_data[month][category] += amount

    def print_report(self, focus_month=None):
        comparisons = self.get_monthly_comparison(focus_month)

        if not comparisons:
            print("No data available for comparison.")
            return

        print("\n📊 Monthly Spending Report\n")

        for comp in comparisons:
            print(f"{comp['from_month']} → {comp['to_month']}")
            print(f"  Current: ${comp['current_total']:.2f}")
            print(f"  Next:    ${comp['next_total']:.2f}")
            print(
                f"  Change:  ${comp['difference']:.2f} "
                f"({comp['percentage_change']:.1f}%)"
            )
            print("-" * 40)

    def get_monthly_comparison(self, focus_month=None):
        months = sorted(self.spending_data.keys())
        comparisons = []

        for i in range(len(months) - 1):
            current_month = months[i]
            next_month = months[i + 1]

            current_total = sum(self.spending_data[current_month].values())
            next_total = sum(self.spending_data[next_month].values())
            difference = next_total - current_total

            if focus_month and focus_month not in (current_month, next_month):
                continue

            comparisons.append({
                "from_month": current_month,
                "to_month": next_month,
                "current_total": current_total,
                "next_total": next_total,
                "difference": difference,
                "percentage_change": (difference / current_total * 100) if current_total > 0 else 0
            })

        return comparisons

    def get_suggestions(self):
        """Generate simple suggestions based on last two months of data."""
        months = sorted(self.spending_data.keys())
        if len(months) < 2:
            return ["Not enough data to generate suggestions."]

        prev_month = months[-2]
        curr_month = months[-1]

        suggestions = []
        for category in self.spending_data[curr_month]:
            prev_amount = self.spending_data[prev_month].get(category, 0)
            curr_amount = self.spending_data[curr_month][category]

            if curr_amount > prev_amount:
                if prev_amount > 0:
                    increase_pct = (curr_amount - prev_amount) / prev_amount * 100
                else:
                    increase_pct = 100.0
                suggestions.append(
                    f"You spent more on {category} this month (+{increase_pct:.1f}%)."
                )

        return suggestions or ["Your spending is stable compared to last month."]

    def export_to_pdf(self, output_path, focus_month=None):
        """Export the spending trend report to a nicely formatted PDF file."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle,
            )
        except ImportError:
            print("[!] PDF export requires the 'reportlab' package. Install it with: pip install reportlab")
            return

        comparisons = self.get_monthly_comparison(focus_month)
        if not comparisons:
            print("No comparison data available to export.")
            return

        suggestions = self.get_suggestions()
        months = sorted(self.spending_data.keys())
        first_month = months[0]
        last_month = months[-1]

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TitleCustom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=colors.HexColor("#003366"),
            alignment=1,
            spaceAfter=16,
        )

        section_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=colors.HexColor("#003366"),
            spaceBefore=12,
            spaceAfter=6,
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
        )

        elements = []

        # Title
        elements.append(Paragraph("SPENDING TREND REPORT", title_style))

        focus_label = focus_month if focus_month else "All months"

        meta_data = [
            ["Period Covered:", f"{first_month} to {last_month}"],
            ["Focus Month:", focus_label],
            ["Generated On:", datetime.now().strftime("%d-%b-%Y %H:%M:%S")],
        ]

        meta_table = Table(meta_data, colWidths=[120, 350])
        meta_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#003366")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ]
            )
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # 1. Executive Summary
        elements.append(Paragraph("1. EXECUTIVE SUMMARY", section_style))
        summary_text = (
            f"This spending trend assessment analyzes monthly expenses from {first_month} to {last_month}. "
            f"It highlights changes in spending between consecutive months and identifies areas where your "
            f"spending has increased or decreased."
        )
        elements.append(Paragraph(summary_text, body_style))

        # 2. Analysis Objective
        elements.append(Paragraph("2. ANALYSIS OBJECTIVE", section_style))
        objective_text = (
            "To compare spending across months, identify significant increases, and provide actionable "
            "suggestions to improve budgeting habits."
        )
        elements.append(Paragraph(objective_text, body_style))

        # 3. Monthly Comparison Details
        elements.append(Paragraph("3. MONTHLY COMPARISON DETAILS", section_style))

        table_data = [
            [
                "From Month",
                "To Month",
                "Previous Total ($)",
                "Current Total ($)",
                "Difference ($)",
                "Change (%)",
            ]
        ]

        for comp in comparisons:
            table_data.append(
                [
                    comp["from_month"],
                    comp["to_month"],
                    f"{comp['current_total']:.2f}",
                    f"{comp['next_total']:.2f}",
                    f"{comp['difference']:+.2f}",
                    f"{comp['percentage_change']:+.1f}",
                ]
            )

        comparison_table = Table(table_data, repeatRows=1)
        comparison_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                    ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                    ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        elements.append(comparison_table)
        elements.append(Spacer(1, 12))

        # 4. Suggestions
        elements.append(Paragraph("4. SUGGESTIONS", section_style))
        if suggestions:
            for s in suggestions:
                elements.append(Paragraph(f"• {s}", body_style))
        else:
            elements.append(Paragraph("No significant changes detected.", body_style))

        doc.build(elements)
        print(f"PDF report saved to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "myExpenses1.csv")
    file_path = os.path.normpath(file_path)

    print("Looking for file at:", file_path)

    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        print("[!] Make sure myExpenses1.csv is inside the data folder.")
    else:
        tracker = SpendingTrend()

        username = input("Enter username to analyze (leave blank for all): ").strip().lower()
        focus_month = input("Enter month to compare (YYYY-MM, leave blank for all): ").strip()
        focus_month = focus_month if focus_month else None

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if username and row.get("username", "").strip().lower() != username:
                    continue

                date_str = (row.get("date") or "").strip()
                amount_str = (row.get("amount") or "0").strip()
                category = (row.get("category") or "Unknown").strip()

                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                month = date_str[:7] if len(date_str) >= 7 else date_str
                if not month:
                    continue

                tracker.add_spending(month, category, amount)
        
        tracker.print_report(focus_month)

        choice = input("Do you want to generate a PDF report? (Yes/No): ").strip().lower()
        if choice in ("yes", "y"):
            safe_user = username or "all_users"
            safe_month = focus_month or "all_months"
            pdf_name = f"spending_trend_{safe_user}_{safe_month}.pdf"

            # Ensure reportPDF directory exists (inside Jomnay)
            report_dir = os.path.join(base_dir, "..", "reportPDF")
            report_dir = os.path.normpath(report_dir)
            os.makedirs(report_dir, exist_ok=True)

            pdf_path = os.path.join(report_dir, pdf_name)
            pdf_path = os.path.normpath(pdf_path)
            tracker.export_to_pdf(pdf_path, focus_month)