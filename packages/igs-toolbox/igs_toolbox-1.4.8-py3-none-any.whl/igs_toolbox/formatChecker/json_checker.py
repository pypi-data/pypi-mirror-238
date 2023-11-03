import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, Union

import jsonschema

import igs_toolbox
from igs_toolbox.formatChecker.seq_metadata_schema import (
    SeqMetadataKeys,
    ValidationError,
    seq_metadata_schema,
)

SCHEMA_NAME = "seqMetadata"


def validate_species(pathogen: str, species: str) -> bool:
    """Validate species field."""
    # get vocabulary for species
    answer_set_path = Path(__file__).parent / f"res/species/txt/answerSet{pathogen}.txt"
    if not answer_set_path.is_file():
        logging.error(f"{answer_set_path} does not point to a file. Aborting.")
        return False

    with Path(answer_set_path).open() as species_file:
        species_list = [line.strip() for line in species_file]

    if species not in species_list:
        logging.error(f"{species} is not a valid species for pathogen {pathogen}.")
        return False
    return True


def check_seq_metadata(
    json_data: Dict[Union[SeqMetadataKeys, str], Any],
    schema: Any = seq_metadata_schema,  # noqa: ANN401
) -> None:
    """Validate the sequence metadata."""
    validator = jsonschema.Draft202012Validator(schema=schema)
    errors = list(validator.iter_errors(json_data))
    error_str = []
    for error in errors:
        if error.validator == "required":
            matched_prop = re.search("'(.*)'", error.message)
            if matched_prop:
                error_str.append("MISSING_" + matched_prop.group(1))
            else:
                error_str.append("MISSING_" + error.message[1 : -len("' is a required property")])
        else:
            error_str.append("INVALID_" + error.relative_path[-1])

    # some validation.py rules cannot be implemented in jsonschema directly,
    # thus check them here programmatically
    if (
        SeqMetadataKeys.SPECIES in json_data
        and SeqMetadataKeys.MELDETATBESTAND in json_data
        and not validate_species(
            json_data[SeqMetadataKeys.MELDETATBESTAND],
            json_data[SeqMetadataKeys.SPECIES],
        )
    ):
        error_str.append("INVALID_SPECIES")

    if len(error_str) > 0:
        raise ValidationError("; ".join(error_str))


# Read command line arguments
def parse(args=None) -> argparse.Namespace:  # noqa: ANN001
    parser = argparse.ArgumentParser(prog=Path(__file__).name.split(".")[0])
    parser.add_argument("-i", "--input", required=True, help="Filepath to json file.")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {igs_toolbox.__version__}",
    )
    args = parser.parse_args(args)
    return args


def main(args=None) -> None:  # noqa: ANN001
    input_file = Path(parse(args).input)
    # read json file
    if not input_file.is_file():
        logging.error(f"{input_file} does not point to a file. Aborting.")
        sys.exit(1)

    with input_file.open() as jsonfile:
        try:
            json_data = json.loads(jsonfile.read())
        except json.decoder.JSONDecodeError:
            logging.exception(f"{input_file} is not a valid json file. Aborting.")
            sys.exit(1)

    # get schema
    try:
        check_seq_metadata(json_data)
    except ValidationError:
        logging.exception(f"FAILURE: JSON file does not adhere to the {SCHEMA_NAME} schema.")
        sys.exit(1)

    logging.info(f"SUCCESS: JSON file adheres to {SCHEMA_NAME} schema.")
    print(f"SUCCESS: JSON file adheres to {SCHEMA_NAME} schema.")  # noqa: T201


if __name__ == "__main__":
    main()
