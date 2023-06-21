# 6.6 for 5 times;
# 7.4 for 10 times;
# 10.1 for 10 * 2 times;
# 9 for 10 * 2 times;

import asyncio
import logging
from newspaper import Source, Config

num_articles = 10 * 2

async def read_article(article):
    await asyncio.to_thread(article.download)
    await asyncio.to_thread(article.parse)
    try:
        publish_date = article.publish_date.strftime('%Y-%m-%d')
    except Exception as exc:
        publish_date = None
        
    title = article.title
    # logging.info(f"Article: {title}, Publish Date: {publish_date}")

    return {'title': title, 'publish_date': publish_date}


async def build_source():
    config = Config()
    config.memoize_articles = False  # Disable article caching

    nyt_source = Source('https://www.nytimes.com', config=config)

    await asyncio.to_thread(nyt_source.build)  # Run in a separate thread

    articles = nyt_source.articles

    return articles


async def main():
    articles = await build_source()
    tasks = []
    for article in articles[:num_articles]:
        tasks.append(asyncio.create_task(read_article(article)))

    results = await asyncio.gather(*tasks)

    # Save results to JSON file
    with open('data/articles.json', 'w') as file:
        json.dump(results, file, indent=4)


await main()
