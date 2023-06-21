# ThreadPoolExecutor()
# 5.9 for 5 times;
# 7.4 for 5 * 2 times;
# 10.2 for 10 * 2 times;
# 8.8 for 10 * 2 times;


import concurrent.futures
import logging
import json
from newspaper import Source, Config

num_articles = 10 * 2

def read_article(article):
    article.download()
    article.parse()
    try:
        publish_date = article.publish_date.strftime('%Y-%m-%d')
    except Exception as exc:
        publish_date = None

    title = article.title

    return {'title': title, 'publish_date': publish_date}


def build_source():
    config = Config()
    config.memoize_articles = False  # Disable article caching

    nyt_source = Source('https://www.nytimes.com', config=config)
    nyt_source.build()

    articles = nyt_source.articles

    return articles


def main():
    articles = build_source()
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = [executor.submit(read_article, article) for article in articles[:num_articles]]

        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            results.append(result)


    # Save results to JSON file
    with open('data/articles.json', 'w') as file:
        json.dump(results, file, indent=4)


main()
