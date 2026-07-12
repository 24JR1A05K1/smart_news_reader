from transformers import pipeline

# Load a lightweight summarization model
summarizer = pipeline(
    "summarization",
    model="Falconsai/text_summarization"
)

def summarize_text(text):
    if not text:
        return "No summary available."

    if len(text.split()) < 40:
        return text

    try:
        summary = summarizer(
            text,
            max_length=60,
            min_length=20,
            do_sample=False
        )

        return summary[0]["summary_text"]

    except Exception as e:
        print("Summarization Error:", e)
        return text