from secrets_to_paper.export import (
    templateEnv,
    write_pdf_to_disk,
)
from secrets_to_paper.export.qr import get_qr_codes
from cryptography.hazmat.primitives.serialization import (
    # PublicFormat,
    Encoding,
    NoEncryption,
    PrivateFormat,
)
import datetime


def export_rsa(private_key, output, key_label=""):
    pemdata = private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.TraditionalOpenSSL,
        NoEncryption(),
    )

    private_numbers = private_key.private_numbers()
    public_numbers = private_key.public_key().public_numbers()

    qr_codes = get_qr_codes(pemdata)

    filename = output + ".pdf"
    template = templateEnv.get_template("rsa_key.html")

    rendered = template.render(
        qr_images=qr_codes,
        ascii_key=pemdata.decode("ascii"),
        key_label=key_label,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        key_type="RSA",
        key_size=private_key.key_size,
        p=hex(private_numbers.p),
        q=hex(private_numbers.q),
        d=hex(private_numbers.d),
        dmp1=hex(private_numbers.dmp1),
        dmq1=hex(private_numbers.dmq1),
        e=hex(public_numbers.e),
        n=hex(public_numbers.n),
    )

    write_pdf_to_disk(rendered, filename)
