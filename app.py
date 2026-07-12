import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, request

from news import get_news, search_news
from summarizer import summarize_text

app = Flask(__name__)

CATEGORIES = [
    "technology",
    "business",
    "sports",
    "health",
    "entertainment",
]


def build_article(article, summarize=False):
    title = article.get("title") or "No Title"
    description = article.get("description") or "No description available."

    if summarize:
        summary = summarize_text(description)
        is_ai_summary = summary.strip() != description.strip()
    else:
        summary = description
        is_ai_summary = False

    return {
        "title": title,
        "summary": summary,
        "image": article.get("urlToImage"),
        "url": article.get("url"),
        "is_ai_summary": is_ai_summary,
    }


@app.route("/")
def home():
    query = request.args.get("query", "").strip()

    if query:
        articles, error = search_news(query)
        news_list = [build_article(article, summarize=True) for article in articles]

        return render_template(
            "index.html",
            search_mode=True,
            query=query,
            news=news_list,
            error=error,
        )

    all_news = {}
    errors = []

    with ThreadPoolExecutor(max_workers=len(CATEGORIES)) as executor:
        future_to_category = {
            executor.submit(get_news, category): category
            for category in CATEGORIES
        }

        for future in future_to_category:
            category = future_to_category[future]
            articles, error = future.result()

            if error and error not in errors:
                errors.append(error)

            news_list = [
                build_article(article, summarize=(index == 0))
                for index, article in enumerate(articles)
            ]
            all_news[category] = news_list

    return render_template(
        "index.html",
        search_mode=False,
        all_news=all_news,
        error=errors[0] if errors else None,
    )


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
