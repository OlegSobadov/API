# Article Filter

> Article Filter is a Python application that filters and displays articles based on various criteria such as date and article content.

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Description

Article Filter is a Python application that allows you to filter articles fetched from the New York Times based on date and article content. It provides options to filter articles by date and check for specific target words or patterns in the article titles. The application provides a graphical user interface (GUI) built with Tkinter for easy interaction.

## Requirements

To run this project, you need to have the following dependencies installed:


- **nltk**: A library for natural language processing. It is used to generate synonyms for filtering articles by content.
- **python-dotenv**: A library for reading environment variables from a .env file. It is used for managing API keys or other sensitive information.
- **newspaper3k**: A library for web scraping and article extraction. It is used to fetch articles from a source.
- ...

## Installation

1. Clone the repository:
git clone https://github.com/your-username/article-filter.git


2. Navigate to the project directory:

cd article-filter


3. Install the required dependencies:

pip install -r requirements.txt


## Usage

1. Run the application:
python main.py


2. The application will open a GUI window with the following options:

- **Filter by Date**: Toggle to enable or disable filtering articles by date.
- **Filter by Article**: Toggle to enable or disable filtering articles by specific target words or patterns.

3. Select the desired filter options.

4. Click the "Filter" button to apply the selected filters and display the filtered articles.


### Command-Line Arguments

The following command-line arguments are available:

- `-n`, `--num_articles`: Number of articles to fetch (default: 5)
- `-d`, `--articles_for_last_days`: Number of days for filtering articles (default: 1)
- `-fd`, `--filter_by_date`: Enable filtering by date (default: False)
- `-fa`, `--filter_by_is_article`: Enable filtering by article (default: False)
- `-t`, `--target`: Target keyword for article filtering


## Configuration

The application provides configuration options that can be modified in the `ArticleFilter` class in the `main.py` file. These options include:

- `num_articles`: The number of articles to display (default: 5).
- `articles_for_last_days`: The number of days in the past to consider when filtering articles (default: 1).
- `filter_by_date`: Toggle to enable or disable filtering articles by date (default: False).
- `filter_by_is_article`: Toggle to enable or disable filtering articles by specific target words or patterns (default: False).
- `target`: The target word or pattern to filter articles by (default: None).

Modify these options according to your requirements before running the application.

## Examples

Here are a few examples demonstrating how to use the Article Filter in the terminal:

- To filter the latest 5 articles published in the last day:

python main.py --num_articles 5 --articles_for_last_days 1 --filter_by_date


- To filter the latest 10 articles published in the last 3 days that contain the word "technology":


python main.py --num_articles 10 --articles_for_last_days 3 --filter_by_date --filter_by_is_article --target "technology"


Feel free to customize the command-line arguments based on your specific requirements.

## Contributing

Contributions to the Article Filter project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
