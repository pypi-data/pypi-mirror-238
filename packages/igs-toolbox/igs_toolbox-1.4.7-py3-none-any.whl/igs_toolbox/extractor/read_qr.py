# Requirements
# mamba install poppler

# Import modules
import argparse
import logging
import sys
from pathlib import Path

import cv2
from pdf2image import convert_from_path

import igs_toolbox


def read_qr_code(filename: str) -> str:
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
    except Exception:  # noqa: BLE001
        return "Error during QR code detection."
    return value


def main(args=None) -> None:  # noqa: ANN001
    input_files = parse(args).files
    for file in input_files:
        if not Path(file).is_file():
            logging.error(f"{file} does not point to a file. Aborting.")
            sys.exit(1)

    # Iterate over files
    if len(input_files) > 0:
        for file in input_files:
            filename = Path(file).name.split(".")[0]
            images = convert_from_path(file)

            # Go through pages and save them as PNG
            for i in range(len(images)):
                page_name = f"{file}_{i!s}.png"
                images[i].save(page_name, "PNG")

                # Detect QR code and print it
                id_value = read_qr_code(page_name)
                print(f"{filename}\t{id_value}")  # noqa: T201
                Path(page_name).unlink()
    else:
        sys.exit(2)


# Read command line arguments
def parse(args=None) -> argparse.Namespace:  # noqa: ANN001
    parser = argparse.ArgumentParser(prog=Path(__file__).name.split(".")[0])
    parser.add_argument("files", nargs="*")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {igs_toolbox.__version__}",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
