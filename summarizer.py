import logging
from functools import lru_cache

from transformers import pipeline

logger = logging.getLogger(__name__)

_summarizer = None
MAX_INPUT_CHARS = 4000
MIN_WORDS_FOR_SUMMARY = 40


def _get_summarizer():
    global _summarizer

    if _summarizer is None:
        logger.info("Loading summarization model...")
        _summarizer = pipeline(
            "summarization",
            model="Falconsai/text_summarization",
        )

    return _summarizer


def _truncate_text(text):
    if len(text) <= MAX_INPUT_CHARS:
        return text

    truncated = text[:MAX_INPUT_CHARS]
    last_space = truncated.rfind(" ")

    if last_space > 0:
        return truncated[:last_space]

    return truncated


@lru_cache(maxsize=128)
def summarize_text(text):
    if not text:
        return "No summary available."

    if len(text.split()) < MIN_WORDS_FOR_SUMMARY:
        return text

    truncated_text = _truncate_text(text)

    try:
        result = _get_summarizer()(
            truncated_text,
            max_length=60,
            min_length=20,
            do_sample=False,
        )
        return result[0]["summary_text"]

    except (IndexError, KeyError, ValueError) as exc:
        logger.warning("Summarization failed: %s", exc)
        return text

    except Exception as exc:
        logger.error("Unexpected summarization error: %s", exc)
        return text
