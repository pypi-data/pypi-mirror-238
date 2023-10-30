import io
import subprocess
import base64
from pyzbar.pyzbar import decode  # type: ignore
import pdfplumber
from PIL import Image
import math
import pathlib
import click
import gpg  # type: ignore


def pdf_to_secret(pdf_file, parse_gpg=False):
    with pdfplumber.open(pdf_file) as pdf:
        private_qr_codes = []
        public_qr_codes = []

        for page in pdf.pages:
            begin = "-----BEGIN PRIVATE QR CODES-----"
            end = "-----END PRIVATE QR CODES-----"

            private_qr_codes += get_codes_between_strings(page, begin, end)

            if parse_gpg:
                # also load the public keys for GPG in order to load with paperkey
                begin = "-----BEGIN PUBLIC QR CODES-----"
                end = "-----END PUBLIC QR CODES-----"

                public_qr_codes += get_codes_between_strings(page, begin, end)

    if parse_gpg:
        # parse qr codes and pass to paperkey for private bits
        # need the public component
        public_key = b"".join([qr.data[2:] for qr in public_qr_codes])
        private_key = b"".join([qr.data[2:] for qr in private_qr_codes])

        with open("public-key.gpg", "wb") as f:
            f.write(public_key)

        # needed to de-armor the gpg key back to binary
        subprocess.run(["gpg", "--dearmor", "public-key.gpg"])

        parsed_gpg = subprocess.run(
            [
                "paperkey",
                "--pubring",
                "public-key.gpg.gpg",
                "--input-type",
                "raw",
            ],
            input=private_key,
            capture_output=True,
        )

        # subprocess.run(["gpg", "--import"], input=parsed_gpg.stdout)

        pubkey_rem = pathlib.Path("public-key.gpg")
        pubkey_rem.unlink()
        pubkey_rem = pathlib.Path("public-key.gpg.gpg")
        pubkey_rem.unlink()

        # with gpg.Context(armor=True) as c:
        #     c.key_import(private_key.decode())

    else:
        # just print the parsed key to stdout, unless outfile then write to disk
        private_key = "".join([qr.data.decode("ascii") for qr in private_qr_codes])

        click.secho(private_key, fg="red")
        # print(private_key)


def get_codes_between_strings(page, begin_string, end_string):
    bbox = get_bounding_box(page.chars, begin_string, end_string)
    filtered_qr_codes = qr_codes_in_bbox(page, bbox)

    return filtered_qr_codes


def get_bounding_box(chars, begin, end):
    text = [char["text"] for char in chars]

    x0 = "".join(text).find(begin)
    x1 = x0 + len(begin) - 1 if x0 >= 0 else -1

    y0 = "".join(text).find(end)
    y1 = y0 + len(end) - 1 if y0 >= 0 else -1

    bbox = {
        "x0": chars[x0]["top"] if x0 >= 0 else math.inf,
        "x1": chars[x1]["top"] if x1 >= 0 else math.inf,
        "y0": chars[y0]["bottom"] if y0 >= 0 else math.inf,
        "y1": chars[y1]["bottom"] if y1 >= 0 else math.inf,
    }

    return bbox


def qr_codes_in_bbox(page, bounding_box):
    qr_codes = []

    for image in page.images:
        if image["top"] > bounding_box["x0"] and image["bottom"] < bounding_box["y0"]:
            img = Image.open(io.BytesIO(image["stream"].rawdata))
            qr_codes += decode(img)

    return qr_codes
