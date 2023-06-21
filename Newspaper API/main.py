import os
import time
import json
import logging
import datetime
from datetime import date, timedelta
from newspaper import Config, Article, Source
from nltk.corpus import wordnet
import re
import tkinter as tk
import argparse


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ArticleFilter:
    """
    Class to filter articles based on various criteria.
    """

    def __init__(self, num_articles=5, articles_for_last_days=1, filter_by_date=False, filter_by_is_article=False, target=None):
        """
        Initialize the ArticleFilter object.

        Args:
            num_articles (int): Number of articles to filter.
            articles_for_last_days (int): Number of past days to consider for filtering.
            filter_by_date (bool): Flag to enable/disable filtering by date.
            filter_by_is_article (bool): Flag to enable/disable filtering by article content.
            target (str): Target keyword for article filtering.
        """
        self.num_articles = num_articles
        self.articles_for_last_days = articles_for_last_days
        self.filter_by_date = filter_by_date
        self.filter_by_is_article = filter_by_is_article
        self.target = target
        self.articles = self.build_source()


    def build_source(self):
        """
        Build the article source and fetch articles.

        Returns:
            list: List of articles from the source.
        """
        config = Config()
        config.memoize_articles = False  # Disable article caching

        # Create a Source object for The New York Times
        nyt_source = Source('https://www.nytimes.com', config=config)

        # Fetch the articles from the source
        nyt_source.build()
        articles = nyt_source.articles
        logger.info(f"Source built. Found {len(articles)} articles.")

        return articles

    def filter_articles(self):
        """
        Filter articles based on the specified criteria and print the filtered results.
        """
        if self.filter_by_is_article and self.target: # use only if switch on to filter by article
                                                        # and target not None
            synonyms_pattern = self.generate_synonyms_pattern(self.target)
            logger.info(f'choisen target to article: {self.target}')

        if self.filter_by_date:
            logger.info(f'choisen filter by date for: {self.articles_for_last_days} days!')

        idx = 1
        for article in self.articles[:self.num_articles]:
            day_ago_date = self.calculate_past_date(delta_days=self.articles_for_last_days)
            print(f"{idx}/{self.num_articles}")
            idx += 1
            article.download()
            article.parse()
            publish_date = article.publish_date.strftime('%Y-%m-%d')
            pub_day = self.parse_day(publish_date)
            cur_day = self.parse_day(day_ago_date)

            if self.filter_by_date and (pub_day != cur_day):
                continue

            if self.filter_by_is_article and not self.is_article(synonyms_pattern, article.title):
                continue

            print(f"published date: {pub_day}\n day ago date: {cur_day}")
            print(f'Title: {article.title}')


    def calculate_past_date(self, delta_days: int):
        """
        Calculate a past date based on the specified number of days.

        Args:
            delta_days (int): Number of days in the past.

        Returns:
            str: Formatted date in the past (YYYY-MM-DD).
        """
        current_date = date.today()
        day_ago = current_date - timedelta(days=delta_days)
        formatted_day = day_ago.strftime('%Y-%m-%d')

        return formatted_day
    
    def generate_synonyms_pattern(self, word):
        """
        Generate a regular expression pattern from the synonyms of a given word.

        Args:
            word (str): Target word for generating synonyms.

        Returns:
            str: Regular expression pattern.
        """
        synonyms = []
        set_temp = set() # skip dublicates
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() not in set_temp:
                    set_temp.add(lemma.name())
                    synonyms.append(lemma.name())

        synonyms_pattern = r'\b' + r'\b|\b'.join(synonyms) + r'\b'
        return synonyms_pattern
    
    def parse_day(self, date: datetime):
        """
        Extract the day from a given datetime object.

        Args:
            date (datetime): Datetime object.

        Returns:
            str: Extracted day.
        """
        return str(date).rsplit('-', 1)[-1]

    def is_article(self, pattern, article):
        """
        Check if the article title matches the specified pattern.

        Args:
            pattern (str): Regular expression pattern.
            article (str): Article title.

        Returns:
            bool: True if the article matches the pattern, False otherwise.
        """
        if re.search(pattern, article, re.IGNORECASE) is not None:
            return True
        return False


def toggle_filter_by_date():
    article_filter.filter_by_date = not article_filter.filter_by_date

def toggle_filter_by_is_article():
    article_filter.filter_by_is_article = not article_filter.filter_by_is_article

def filter_articles():
    article_filter.filter_articles()


if __name__ == '__main__':
    # Create command-line argument parser
    parser = argparse.ArgumentParser(description='Article Filter')
    parser.add_argument('-n', '--num_articles', type=int, default=5, help='Number of articles to fetch')
    parser.add_argument('-d', '--articles_for_last_days', type=int, default=1,
                        help='Number of days for filtering articles')
    parser.add_argument('-fd', '--filter_by_date', action='store_true', help='Enable filtering by date')
    parser.add_argument('-fa', '--filter_by_is_article', action='store_true', help='Enable filtering by article')
    parser.add_argument('-t', '--target', type=str, help='Target keyword for article filtering')

    args = parser.parse_args()

    # Create Tkinter window
    window = tk.Tk()

    # Create ArticleFilter instance
    article_filter = ArticleFilter(
        num_articles=args.num_articles,
        articles_for_last_days=args.articles_for_last_days,
        filter_by_date=args.filter_by_date,
        filter_by_is_article=args.filter_by_is_article,
        target=args.target
    )

    # Create switches using Tkinter Checkbuttons
    date_switch = tk.Checkbutton(window, text="Filter by Date", command=toggle_filter_by_date)
    date_switch.pack()

    article_switch = tk.Checkbutton(window, text="Filter by Article", command=toggle_filter_by_is_article)
    article_switch.pack()

    # Create Filter button
    filter_button = tk.Button(window, text="Filter", command=filter_articles)
    filter_button.pack()

    window.mainloop()