import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import tomllib
from loguru import logger


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

class MessageAnalysis:
    def __init__(self, df: pd.DataFrame, keyword: str, img_dir: Path):
        self.df = df
        self.keyword = keyword
        self.img_dir = img_dir
        self.img_dir.mkdir(parents=True, exist_ok=True)  # make sure folder exists

    def add_features(self):
        self.df["hour"] = self.df["timestamp"].dt.hour
        self.df["msg_length"] = self.df["message"].str.len()
        return self.df

    def plot_distribution_by_hour(self):
        keyword_hours = self.df[self.df["message"].str.contains(self.keyword, case=False)]["hour"].astype(int)
        plt.figure(figsize=(10, 6))
        sns.histplot(keyword_hours, bins=24, kde=False, color="skyblue")
        plt.xlabel("Hour of Day")
        plt.ylabel("Frequency")
        plt.title(f"Flatgebouw App-groep gonst: '{self.keyword}' nieuws rond de klok")
        plt.xticks(range(0, 24))
        save_path = self.img_dir / f"{self.keyword}_histogram_by_hour_wk2.png"
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved histogram plot to {save_path}")

    def plot_trend(self):
        keyword_df = self.df[self.df["message"].str.contains(self.keyword, case=False)]
        trend_df = keyword_df.set_index("timestamp").resample("D").size().reset_index(name="count")

        if trend_df.empty:
            logger.warning(f"No messages found for keyword '{self.keyword}'.")
            return

        max_row = trend_df.loc[trend_df["count"].idxmax()]
        max_date = max_row["timestamp"].strftime("%Y-%m-%d")
        max_count = max_row["count"]

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=trend_df, x="timestamp", y="count", marker="o")
        plt.xlabel("Date")
        plt.ylabel(f"Number of '{self.keyword}' Messages")
        plt.title(f"'{self.keyword}' gesprekken door de jaren heen")
        plt.xticks(rotation=45)

        avg_count = trend_df["count"].mean()
        plt.axhline(y=avg_count, color="blue", linestyle="--", linewidth=1.5, label=f"Average ({avg_count:.1f})")
        plt.annotate(
            f"Peak: Lift deurdrangers vervangen on {max_date}",
            xy=(max_row["timestamp"], max_count),
            xytext=(max_row["timestamp"] + pd.Timedelta(days=7), max_count),
            arrowprops=dict(arrowstyle="->", color="red"),
            va="center"
        )
        plt.legend()
        save_path = self.img_dir / f"{self.keyword}_trend_wk2.png"
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved trend plot to {save_path}")

    def scatter_message_length(self):
        keyword_msgs = self.df[self.df["message"].str.contains(self.keyword, case=False)]
        plt.figure(figsize=(10, 6))
        plt.scatter(keyword_msgs["hour"], keyword_msgs["msg_length"], alpha=0.6)
        plt.xlabel("Hour of Day")
        plt.ylabel("Message Length")
        plt.title(f"De '{self.keyword}' zorgt voor golf aan berichten, en stapelt zich op!")
        save_path = self.img_dir / f"{self.keyword}_scatter_length_vs_hour_wk2.png"
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved scatter plot to {save_path}")


def main():

    # Define log file path
    log_file_path = Path(__file__).parent / "logs" / "logfile.log"
    log_file_path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists

    # Add logger to write messages to file
    logger.add(log_file_path, rotation="10 MB", retention="10 days", level="INFO", encoding="utf-8")

    # Load keyword from command-line argument with restricted choices
    parser = argparse.ArgumentParser(description="Analyze messages by keyword")
    parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        choices=["lift", "schoon", "camera"],  # only allow these keywords
        help="Keyword to analyze: 'lift', 'schoon' or 'camera'"
    )
    args = parser.parse_args()

    config_loader = ConfigLoader(Path.cwd() / "config.toml")
    config = config_loader.load()

    # Load data
    data_handler = DataHandler(config)
    logger.info(f"Loading data from {data_handler.datafile}")
    df = data_handler.load_data()

    keyword = args.keyword
    logger.info(f"=== Analyzing keyword: '{keyword}' ===")
    img_dir = Path.cwd() / "img"
    analysis = MessageAnalysis(df, keyword, img_dir)
    analysis.add_features()
    analysis.plot_distribution_by_hour()
    analysis.plot_trend()
    analysis.scatter_message_length()

    logger.info("Done!") 

if __name__ == "__main__":
    main()
