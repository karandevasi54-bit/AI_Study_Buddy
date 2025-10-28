SUMMARY_PROMPT = """Summarize the following study notes into:
• 5-10 bullet points
• One detailed paragraph
• 3-5 key concepts
• 3 study tips

Text:
{content}"""

MCQ_PROMPT = """Create {n} multiple-choice questions from this text.
Each with 4 options (A–D) and mark the correct answer.

Text:
{content}"""
