"""A script to analyse book data."""

import logging
import pandas as pd
from pandas import DataFrame
import altair as alt


log_handlers = [logging.StreamHandler()]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=log_handlers
)
logger = logging.getLogger(__name__)


def load_csv(file_path: str) -> DataFrame:
    """Loads CSV into a pandas DataFrame."""
    df = pd.read_csv(file_path)
    return df


def add_decade_column(df: DataFrame) -> DataFrame:
    """Adds a decade column based on the 'Year' column."""
    df["Decade"] = (df["year"] // 10) * 10
    return df


def plot_decade_pie_chart(df: DataFrame, filename: str = "decade_releases.png"):
    """Creates a pie chart showing the proportion of books released in each decade."""
    decade_counts = df["Decade"].value_counts().reset_index()
    decade_counts.columns = ["Decade", "Count"]

    chart = alt.Chart(decade_counts).mark_arc().encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Decade", type="nominal", legend=None),
        tooltip=["Decade", "Count"]
    ).properties(
        title="Book Releases by Decade"
    )

    chart.save(filename)
    logger.info("Saved: %s", filename)


def plot_top_authors_bar_chart(df: DataFrame, filename: str = "top_authors.png"):
    """Creates a sorted bar chart of total number of ratings for the ten most-rated authors."""
    author_counts = df["author_name"].value_counts().nlargest(10).reset_index()
    author_counts.columns = ["author_name", "Count"]

    chart = alt.Chart(author_counts).mark_bar().encode(
        x=alt.X("Count:Q", title="Number of Books"),
        y=alt.Y("author_name:N", sort="-x"),
        tooltip=["author_name", "Count"]
    ).properties(
        title="Top 10 Most-Rated Authors",
        width=600,
        height=400
    )

    chart.save(filename)
    logger.info("Saved: %s", filename)


if __name__ == "__main__":
    try:
        logger.info("Loading data...")
        dataframe = load_csv("PROCESSED_DATA.csv")

        logger.info("Processing decades...")
        dataframe = add_decade_column(dataframe)
        plot_decade_pie_chart(dataframe)

        logger.info("Processing authors...")
        plot_top_authors_bar_chart(dataframe)

    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
