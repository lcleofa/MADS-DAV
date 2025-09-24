import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer
from loguru import logger
import tomllib

class ConfigLoader:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = None

    def load(self):
        with self.config_path.open("rb") as f:
            self.config = tomllib.load(f)
        return self.config

class DataHandler:
    def __init__(self, config: dict):
        # Use current working directory (project root)
        project_root = Path.cwd() 
        self.datafile = project_root / config["processed"] / config["current"]
        
    def load_data(self):
        if not self.datafile.exists():
            raise FileNotFoundError(
                f"{self.datafile} does not exist. Run src/preprocess.py first and check the timestamp!"
            )
        df = pd.read_parquet(self.datafile)
        return df

class SentimentAnalyzerNL:
    """Compute sentiment for Dutch text messages using TextBlob-NL."""

    def __init__(self, df: pd.DataFrame, keywords: list[str]):
        self.df = df.copy()
        self.keywords = keywords
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        self.monthly_sentiment = None

    def sentiment_nl(self, text: str) -> float:
        blob = TextBlob(str(text), pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        return blob.sentiment[0]

    def compute_keyword_sentiment(self):
        self.df["sentiment"] = self.df["message"].apply(self.sentiment_nl)
        for kw in self.keywords:
            self.df[kw] = self.df["message"].apply(
                lambda m: self.sentiment_nl(m) if kw.lower() in str(m).lower() else np.nan
            )
        return self.df[["timestamp", "message"] + self.keywords + ["sentiment"]]

    def resample_monthly_sentiment(self):
        df_keywords = self.df.set_index("timestamp")
        self.monthly_sentiment = df_keywords[self.keywords].resample("ME").mean()
        return self.monthly_sentiment

    def filter_cooccurring_months(self):
        return self.monthly_sentiment.dropna(subset=self.keywords)

    def plot_rolling_sentiment(self, window: int = 3, save_dir: Path | None = None):
        """Plot rolling mean sentiment trends for keywords and save the plot (do not display)."""
        if self.monthly_sentiment is None:
            raise ValueError("Monthly sentiment not computed. Call resample_monthly_sentiment() first.")

        # Use non-interactive backend to avoid showing the plot
        plt.switch_backend("Agg")

        plt.figure(figsize=(12, 6))
        monthly_sentiment = self.monthly_sentiment.copy()
        monthly_sentiment.index = monthly_sentiment.index.tz_localize(None)

        label_map = {
            "schoon": "Hygiëne",
            "dank": "Waardering"
        }

        for kw in self.keywords:
            series = monthly_sentiment[kw].dropna()
            smoothed = series.rolling(window=window, min_periods=1, center=True).mean()
            plt.plot(
                smoothed.index,
                smoothed.values,
                "-",
                linewidth=2,
                label=f"{label_map.get(kw, kw)} (`{kw}`)"
            )

        plt.axhline(y=0, color="gray", linestyle="--", label="Neutraal sentiment")
        plt.xlabel("Datum")
        plt.ylabel("Gemiddeld sentiment (-1 negatief, +1 positief)")
        plt.title("Sentiment trends over hygiëne en waardering in een flatgebouw!")
        plt.legend()
        ax = plt.gca()
        ax.yaxis.set_major_locator(MultipleLocator(0.05))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot if save_dir is provided
        if save_dir:
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = save_dir / f"sentiment_plot_{'_'.join(self.keywords)}_wk3.png"
            plt.savefig(file_path, dpi=300)
            logger.info(f"Plot saved to {file_path}")

        # Do NOT call plt.show()
        plt.close()

def main():

    # Define log file path
    log_file_path = Path(__file__).parent / "logs" / "logfile.log"
    log_file_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

    # Add logger to write messages to file
    logger.add(log_file_path, rotation="10 MB", retention="10 days", level="INFO", encoding="utf-8")

    # Load keywords from command-line argument (allow multiple)
    parser = argparse.ArgumentParser(description="Analyze messages by keyword")
    parser.add_argument(
        "--keywords",
        "-k",
        type=str,
        nargs="+",  # allow one or more keywords
        required=True,
        choices=["lift", "schoon", "camera", "dank"],
        help="Keywords to analyze (choose one or more). Example: -k schoon dank"
    )
    args = parser.parse_args()

    # Load config
    config_loader = ConfigLoader(Path.cwd() / "config.toml")
    config = config_loader.load()

    # Load data
    data_handler = DataHandler(config)
    logger.info(f"Loading data from {data_handler.datafile}")
    df = data_handler.load_data()

    keywords = args.keywords
    logger.info(f"=== Analyzing keywords: {keywords} ===")

    # Create analyzer and run
    analyzer = SentimentAnalyzerNL(df, keywords)
    analyzer.compute_keyword_sentiment()
    analyzer.resample_monthly_sentiment()
    analyzer.plot_rolling_sentiment()

    img_dir = Path.cwd() / "img"
    analyzer.plot_rolling_sentiment(save_dir=img_dir)


if __name__ == "__main__":
    main()
