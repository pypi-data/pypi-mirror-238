from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    PublicFormat,
    Encoding,
    NoEncryption,
    PrivateFormat,
)

# You can find the definition in RFC 5915. It defines an ECPrivateKey object:

# ECPrivateKey ::= SEQUENCE {
#  version        INTEGER { ecPrivkeyVer1(1) } (ecPrivkeyVer1),
#  privateKey     OCTET STRING,
#  parameters [0] ECParameters {{ NamedCurve }} OPTIONAL,
#  publicKey  [1] BIT STRING OPTIONAL
# }

from cryptography.hazmat.primitives.asymmetric.ec import (
    SECP256R1,
    EllipticCurvePrivateKey,
    derive_private_key,
)


def build_ecc_key(
    secret_number=None,
    private_key: EllipticCurvePrivateKey | None = None,
    curve="secp256r1",
):
    if curve == "secp256r1":
        curve = SECP256R1()
    else:
        raise NotImplementedError("Curve type not implemented.")

    if secret_number:
        secret_int = int(secret_number, 16)
        priv_key = derive_private_key(secret_int, curve, default_backend())
    elif private_key:
        priv_key = private_key

    # Make private and public keys from the private value + curve
    pub_key = priv_key.public_key()

    pubkey = pub_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")

    # derived_key = derive_private_key(secret_int, SECP256R1(), default_backend())
    private_key_decoded = priv_key.private_bytes(
        Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()
    ).decode("ascii")

    print(pubkey)
    print(private_key_decoded)
