from flask import Flask, render_template, request
from news import get_news, search_news
from summarizer import summarize_text

app = Flask(__name__)

@app.route("/")
def home():

    query = request.args.get("query")

    # ---------------- SEARCH MODE ---------------- #
    if query:

        articles = search_news(query)

        news_list = []

        for article in articles:

            title = article.get("title", "No Title")
            description = article.get("description") or "No description available."

            summary = summarize_text(description)

            news_list.append({
                "title": title,
                "summary": summary,
                "image": article.get("urlToImage"),
                "url": article.get("url")
            })

        return render_template(
            "index.html",
            search_mode=True,
            query=query,
            news=news_list
        )

    # ---------------- CATEGORY MODE ---------------- #

    categories = [
        "technology",
        "business",
        "sports",
        "health",
        "entertainment"
    ]

    all_news = {}

    for category in categories:

        articles = get_news(category)

        news_list = []

        for index, article in enumerate(articles):

            title = article.get("title", "No Title")
            description = article.get("description") or "No description available."

            if index == 0:
                summary = summarize_text(description)
            else:
                summary = description

            news_list.append({
                "title": title,
                "summary": summary,
                "image": article.get("urlToImage"),
                "url": article.get("url")
            })

        all_news[category] = news_list

    return render_template(
        "index.html",
        search_mode=False,
        all_news=all_news
    )

if __name__ == "__main__":
    app.run(debug=True)