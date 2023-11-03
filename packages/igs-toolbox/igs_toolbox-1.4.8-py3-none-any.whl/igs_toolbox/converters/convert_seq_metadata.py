import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from zoneinfo import ZoneInfo

import igs_toolbox
from igs_toolbox.formatChecker import json_checker
from igs_toolbox.formatChecker.seq_metadata_schema import ValidationError

sys.path.append(Path(__file__).resolve().parent.parent)


# Read command line arguments
def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Filepath to xlsx file.")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Filepath to output folder for json files.",
    )
    parser.add_argument(
        "-e",
        "--error_log",
        required=False,
        help="Filepath to log file.",
        default=datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%d%m%Y%H%M%S") + ".log",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {igs_toolbox.__version__}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse()
    logging.basicConfig(
        filename=args.error_log,
        encoding="utf-8",
        level=logging.ERROR,
        format="%(message)s",
        force=True,
    )
    # read json file
    if not Path(args.input).is_file():
        print(f"{args.input} does not point to a file. Aborting.")  # noqa: T201
        sys.exit(1)

    Path(args.output).mkdir(parents=True, exist_ok=True)

    meta_df = pd.read_excel(args.input, dtype=str)
    meta_dict = meta_df.to_dict(orient="records")
    for entry_dict in meta_dict:
        sample_id = entry_dict["LAB_SEQUENCE_ID"]
        # replace NANs
        clean_dict = {k: entry_dict[k] for k in entry_dict if not pd.isna(entry_dict[k])}
        try:
            json_checker.check_seq_metadata(clean_dict)
            with (Path(args.outpu) / sample_id + "_sequencing_metadata.json").open("w") as outfile:
                json.dump(clean_dict, outfile, indent=4)
        except ValidationError:
            logging.exception("Invalid data")


if __name__ == "__main__":
    main()
