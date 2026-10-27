from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from xml.sax.saxutils import escape

def make_report(result):
    buffer=BytesIO()
    doc=SimpleDocTemplate(buffer,pagesize=(595,842),rightMargin=42,leftMargin=42)
    styles=getSampleStyleSheet()
    story=[Paragraph("GhostTrace | Privacy Scan Report",styles["Title"]),Spacer(1,16)]
    for key,val in [("File",result["filename"]),("Type",result["filetype"]),("Risk",result["risk"]),("Score",str(result["score"])+"/100"),("SHA-256",result["sha256"])]:
        story.append(Paragraph(f"<b>{escape(key)}:</b> {escape(str(val))}",styles["Normal"]))
        story.append(Spacer(1,8))
    story.append(Spacer(1,10))
    story.append(Paragraph("Detected findings",styles["Heading2"]))
    if not result["findings"]:
        story.append(Paragraph("No supported risk indicators detected. This does not prove the file is safe.",styles["Normal"]))
    for f in result["findings"]:
        story.append(Paragraph(f"<b>{escape(f['type'])} ({escape(f['severity'])})</b>: {escape(f['detail'])} | Count: {f['count']}",styles["Normal"]))
        story.append(Spacer(1,9))
    story.append(Spacer(1,15))
    story.append(Paragraph("Privacy note: Pattern matches are heuristic, may be false positives, and do not establish identity or malicious intent. File contents are analyzed locally and not stored in the database.",styles["Normal"]))
    doc.build(story)
    return buffer.getvalue()
