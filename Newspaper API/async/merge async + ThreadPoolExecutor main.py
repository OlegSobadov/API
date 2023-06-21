# merge async + concurrent.futures.ThreadPoolExecutor()
# 9.4 for 10 * 2 times;
# 8.7 for 10 * 2 times; # second run;


import asyncio
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


async def process_articles():
    articles = build_source()
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(executor, read_article, article) for article in articles[:num_articles]]

        results = await asyncio.gather(*tasks)

    return results


async def main():
    results = await process_articles()

    # Save results to JSON file
    with open('data/articles.json', 'w') as file:
        json.dump(results, file, indent=4)





await main()
