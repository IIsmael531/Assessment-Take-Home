"""A script to process book data."""

import csv
import sqlite3
from sqlite3 import connect
import logging
import argparse


log_handlers = [logging.StreamHandler()]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=log_handlers
)
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(
    description="Filepath")
parser.add_argument(
    "-f", "--filepath", required=True, help="Input the filepath of the file you want to process")
args = parser.parse_args()
file_path = args.filepath


def download_csv(file_path: str) -> list[list[str]]:
    """Reads the file provided, skips the first row, and returns the remaining data"""
    logger.info("Loading data from CSV...")

    with open(file_path, 'r', newline='', encoding="UTF_8") as infile:
        reader = csv.reader(infile)
        next(reader)
        data = list(reader)
        logger.info("Loaded %d rows from CSV.", len(data))
        return data


def remove_information_in_brackets(title: str) -> str:
    """Removes any characters within brackets"""
    result = ''
    inside_brackets = False

    for char in title:
        if char == '(':
            inside_brackets = True
        elif char == ')':
            inside_brackets = False
        elif not inside_brackets:
            result += char
    return result.strip()


def get_author_name(author_id: int) -> str:
    """Retrieves the author name from author id"""

    query = 'SELECT name FROM author WHERE id = ?'
    cursor.execute(query, (author_id,))
    result = cursor.fetchone()
    return result[0]


def clean_data(data: list[list[str]]) -> list[list]:
    """Cleans and formats the data given"""

    final = []

    logger.info("Cleaning data...")

    for row in data:
        row = row[3:]

        if '' in row:
            continue

        try:
            row[0] = remove_information_in_brackets(row[0])
            row[1] = get_author_name(int(float(row[1])))
            row[2] = int(row[2])
            row[3] = float(row[3].replace(',', '.'))
            row[4] = int(row[4].strip('`'))
        except (ValueError, IndexError, TypeError, sqlite3.Error) as e:
            logger.warning("Skipping row due to error: %s | Row: %s", e, row)
            continue

        else:
            final.append(row)

    logger.info("Cleaning complete. %d valid rows retained.", len(final))
    return final


def desc_order(data: list[list], column_number: int = 3) -> list:
    """Orders the output by a chosen column_number in descending order"""
    logger.info("Sorting data by rating...")
    return sorted(data, key=lambda row: row[column_number], reverse=True)


def write_csv(data, filename: str = "PROCESSED_DATA.csv"):
    """writes a csv file with the data provided"""

    logger.info("Writing cleaned data to: %s", filename)
    with open(filename, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['title', 'author_name', 'year', 'rating', 'ratings'])
        writer.writerows(data)


if __name__ == "__main__":

    try:
        sqliteConnection = connect('data/authors.db')
        cursor = sqliteConnection.cursor()
        logger.info("Database connection established.")

        cleaned_data = clean_data(download_csv(file_path))
        # "data/RAW_DATA_1.csv"
        sorted_data = desc_order(cleaned_data)
        write_csv(sorted_data)

        cursor.close()

    except sqlite3.Error as error:
        logger.error("Error occurred during DB sequence %s", error)

    finally:

        if sqliteConnection:
            sqliteConnection.close()
            logger.info("SQLite connection closed.")
