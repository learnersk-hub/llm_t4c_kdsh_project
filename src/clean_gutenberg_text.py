def clean_gutenberg_text(text):
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx != -1:
        # move index to AFTER the start marker line
        start_idx = text.find("\n", start_idx) + 1

    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx]

    return text.strip()
