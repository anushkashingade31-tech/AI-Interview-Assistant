from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape


def generate_pdf(user_name, answers, average_score, output_path):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(output_path)

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "<b>AI Interview Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Candidate:</b> {escape(str(user_name))}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Average Score:</b> {average_score:.2f}/10",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------
    # Questions
    # -----------------------------

    for i, ans in enumerate(answers):

        story.append(
            Paragraph(
                f"<b>Question {i + 1}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                escape(str(ans.get("question", ""))),
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                "<b>Your Answer</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                escape(str(ans.get("user_answer", ""))),
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                f"<b>AI Score:</b> {ans.get('ai_score', 0)}/10",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                "<b>Feedback</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                escape(str(ans.get("feedback", ""))),
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                "<b>Ideal Answer</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                escape(str(ans.get("ideal_answer", ""))),
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

    # -----------------------------
    # Build PDF
    # -----------------------------

    doc.build(story)