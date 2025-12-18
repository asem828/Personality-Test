from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from characterify.utils.paths import AppPaths


@dataclass
class PdfReportService:
    paths: AppPaths

    def create_report(
        self,
        user_name: str,
        user_email: str,
        test_title: str,
        result_payload: Dict[str, Any],
        created_at_iso: Optional[str] = None,
    ) -> Path:
        """Generate a shareable PDF report (offline)."""

        created_at_iso = created_at_iso or datetime.utcnow().isoformat()
        timestamp = created_at_iso.replace(":", "").replace("-", "").split(".")[0]
        filename = f"Characterify_{result_payload.get('test_id','test')}_{timestamp}.pdf"
        out_path = self.paths.exports_dir / filename

        chart_path = self._render_chart_png(result_payload, suffix=timestamp)

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
        from reportlab.platypus.flowables import HRFlowable

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
        )
        h2 = ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
        )
        normal = ParagraphStyle(
            "Normal",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
        )

        doc = SimpleDocTemplate(str(out_path), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
        story = []

        story.append(Paragraph("Characterify — Personality Report", title_style))
        story.append(Paragraph(f"<b>User</b>: {user_name} &lt;{user_email}&gt;", normal))
        story.append(Paragraph(f"<b>Test</b>: {test_title}", normal))
        story.append(Paragraph(f"<b>Generated</b>: {created_at_iso}", normal))
        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#DDDDDD")))
        story.append(Spacer(1, 12))

        # Result headline
        content = result_payload.get("content", {})
        story.append(Paragraph(f"<b>Result</b>: {result_payload.get('result_type','-')}", h2))
        summary = content.get("summary_md", "")
        summary_html = self._md_to_simple_html(summary)
        story.append(Paragraph(summary_html, normal))
        story.append(Spacer(1, 12))

        if chart_path and chart_path.exists():
            story.append(Paragraph("Score Chart", h2))
            story.append(Spacer(1, 6))
            story.append(Image(str(chart_path), width=16 * cm, height=9 * cm))
            story.append(Spacer(1, 12))

        # Sections
        for section in content.get("sections", []):
            story.append(Paragraph(section.get("title", ""), h2))
            items = section.get("items", [])
            if items:
                bullet_html = "<br/>".join([f"• {self._escape(i)}" for i in items])
                story.append(Paragraph(bullet_html, normal))
            story.append(Spacer(1, 10))

        doc.build(story)
        return out_path

    def _render_chart_png(self, result_payload: Dict[str, Any], suffix: str) -> Optional[Path]:
        """Render matplotlib chart to PNG for embedding in PDF."""

        chart_kind = result_payload.get("chart_kind", "")
        out = self.paths.temp_dir / f"chart_{result_payload.get('test_id','test')}_{suffix}.png"

        # Use Agg backend (safe for headless PDF generation)
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 4.5))
        try:
            if chart_kind == "mbti_stacked":
                dims = result_payload.get("percentages", [])
                labels = [f"{d['name_a']} vs {d['name_b']}" for d in dims]
                y = list(range(len(dims)))
                for i, d in enumerate(dims):
                    plt.barh(i, d["pct_a"], color="#1DB954")
                    plt.barh(i, d["pct_b"], left=d["pct_a"], color="#3A3A3A")
                    plt.text(d["pct_a"] / 2, i, f"{d['name_a']} {d['pct_a']:.0f}%", ha="center", va="center", color="white", fontsize=9)
                    plt.text(d["pct_a"] + d["pct_b"] / 2, i, f"{d['name_b']} {d['pct_b']:.0f}%", ha="center", va="center", color="white", fontsize=9)
                plt.xlim(0, 100)
                plt.yticks(y, labels, fontsize=9)
                plt.xticks([])
                plt.grid(False)
                plt.box(False)
            else:
                # barh chart for OCEAN/Enneagram/Temperament
                if isinstance(result_payload.get("percentages"), dict):
                    perc = result_payload["percentages"]
                    labels = []
                    vals = []
                    for k, v in perc.items():
                        labels.append(str(k))
                        vals.append(float(v))
                    plt.barh(labels, vals, color="#1DB954")
                    plt.xlim(0, max(100, max(vals) + 10 if vals else 100))
                    plt.xticks([])
                    plt.grid(False)
                    plt.box(False)
                else:
                    # already list? fallback
                    plt.text(0.1, 0.5, "Chart unavailable", fontsize=12)

            plt.tight_layout()
            plt.savefig(out, bbox_inches="tight", transparent=False, dpi=150)
            return out
        finally:
            plt.close()

    @staticmethod
    def _escape(text: str) -> str:
        return (
            str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def _md_to_simple_html(self, md: str) -> str:
        """Very small Markdown-to-HTML helper (bold + line breaks)."""

        # Convert **bold**
        html = md.replace("\n", "<br/>")
        # naive bold
        while "**" in html:
            html = html.replace("**", "<b>", 1).replace("**", "</b>", 1)
        return html
