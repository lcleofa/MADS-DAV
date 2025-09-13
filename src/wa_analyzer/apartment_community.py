import re
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import click
import pandas as pd
from loguru import logger

from wa_analyzer.settings import (BaseRegexes, Folders, PreprocessConfig,
                                  androidRegexes, csvRegexes, iosRegexes,
                                  oldRegexes)

logger.remove()
logger.add("logs/logfile.log", rotation="1 week", level="DEBUG")
logger.add(sys.stderr, level="INFO")

logger.debug(f"Python path: {sys.path}")


@click.command()
@click.option(
    "--category", 
    type=click.Choice(["facilities", "hygiene", "safety"]), 
    required=True,
    help="Choose the category of messages to analyze"
)
@click.option(
    "--output", 
    default="img/plot.png", 
    show_default=True,
    help="Path to save the generated visualization"
)
def main(category, output):
    """
    Analyze WhatsApp messages by category and save a visualization.
    """
    click.echo(f"Analyzing category: {category}")
    click.echo(f"Saving plot to: {output}")

    # Example: here you would load your dataframe and generate the plot
    # df = pd.read_csv("data/messages.csv")
    # plot_category(df, category, output)
    # For now just simulate
    click.echo("✅ Done!")

if __name__ == "__main__":
    main()
