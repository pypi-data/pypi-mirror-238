import subprocess
import base64
import datetime
import gpg  # type: ignore
import sys
import os

from secrets_to_paper.export.qr import get_qr_codes
from secrets_to_paper.export import templateEnv, templateLoader, write_pdf_to_disk


def render_gpg_html(
    paperkey_b16,
    ascii_key,
    qr_images=[],
    public_qr_images=[],
    public_key_ascii="",
    key_id="",
    timestamp=None,
):
    template = templateEnv.get_template("gpg_key.html")

    rendered = template.render(
        qr_images=qr_images,
        paperkey_b16=paperkey_b16,
        ascii_key=ascii_key,
        public_key_ascii=public_key_ascii,
        key_id=key_id,
        public_qr_images=public_qr_images,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    )

    return rendered


def export_gpg(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    with gpg.Context(armor=True) as c:
        secret_key_raw = c.key_export_secret(pattern=key_id)

        # # used for producing QR codes (paperkey pulls relevant secret bits)
        # paperkey_raw = subprocess.run(
        #     ["paperkey", "--output-type", "raw"], input=secret_key_raw, capture_output=True
        # )
        qr_codes = get_qr_codes(secret_key_raw)

        # # used for produces textual output
        # paperkey = subprocess.run(
        #     ["paperkey", "--output-type", "base16"],
        #     input=secret_key_raw,
        #     capture_output=True,
        # )
        # paperkey_output = paperkey.stdout.decode("utf-8")

    with gpg.Context(armor=True) as c:
        print(" - Export %s's public keys - " % key_id)
        secret_key = c.key_export_secret(pattern=key_id)
        print(secret_key.decode())

        public_key = c.key_export_minimal(pattern=key_id)
        print(public_key.decode())

        public_qr_codes = get_qr_codes(public_key)


        filename = key_id + ".pdf"

        rendered = render_gpg_html(
            "",
            secret_key.decode('ascii'),
            public_key_ascii=public_key.decode("ascii"),
            qr_images=qr_codes,
            public_qr_images=public_qr_codes,
            key_id=key_id,
        )

        write_pdf_to_disk(rendered, filename)
