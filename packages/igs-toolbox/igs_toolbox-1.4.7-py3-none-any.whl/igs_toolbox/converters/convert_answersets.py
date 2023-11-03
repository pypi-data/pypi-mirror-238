import argparse
import json
from pathlib import Path

import igs_toolbox


# Read command line arguments
def parse() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        help="Filepath to folder with answerset json files.",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=True,
        help="Filepath to output_path folder for answerset txt files.",
    )
    parser.add_argument(
        "-s",
        "--species",
        nargs="+",
        help="List of species for which to convert answersets.",
        default=[
            "EHCP",
            "LISP",
            "SALP",
            "STYP",
            "INVP",
            "NEIP",
            "MSVP",
            "MYTP",
            "CVDP",
            "HIVP",
            "NEGP",
            "EBCP",
            "ACBP",
            "CDFP",
            "MRAP",
            "SALP",
            "HEVP",
            "HAVP",
            "LEGP",
            "SPNP",
            "WNVP",
        ],
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {igs_toolbox.__version__}",
    )
    return parser.parse_args()


def convert_answerset(observation: str, input_path: str, output_path: str) -> None:
    # get vocabulary for species
    answerset_path = Path(input_path) / f"answerSet{observation}.json"
    if not answerset_path.is_file():
        print(f"{answerset_path} does not point to a file. Aborting.")  # noqa: T201
        return

    with answerset_path.open() as jsonfile:
        try:
            answerset = json.loads(jsonfile.read())
        except json.decoder.JSONDecodeError:
            print(f"{answerset_path} is not a valid json file. Aborting.")  # noqa: T201
            return
    answerset_list = [species["display"] for species in answerset["compose"]["include"][0]["concept"]]

    # open file in write mode
    with (Path(output_path) / f"answerSet{observation}.txt").open("w") as fp:
        for item in answerset_list:
            # write each item on a new line
            fp.write(f"{item}\n")
        print(f"Converted {answerset_path}")  # noqa: T201


def main() -> None:
    args = parse()
    Path(args.output_path).mkdir(parents=True, exist_ok=True)
    for obs in args.species:
        convert_answerset(obs, args.input_path, args.output_path)


if __name__ == "__main__":
    main()
