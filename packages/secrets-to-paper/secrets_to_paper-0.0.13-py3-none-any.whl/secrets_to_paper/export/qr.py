import base64
import io
import qrcode


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def get_qr_codes(data):
    """
    Expects binary data to be chunked into a list of base64 image strings
    """

    MAX_QR_BITS = 450
    chunks = (len(data) // MAX_QR_BITS) + 1

    qr_codes = []
    split_data = list(split(data, chunks))
    for i, chunk in enumerate(split_data):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=2,
            border=4,
        )

        # first byte is what chunk, second byte is how many chunks
        current_chunk_prefix = bytes([i + 1])
        chunk_total_prefix = bytes([chunks])
        qr_data = base64.b64encode(
            current_chunk_prefix + chunk_total_prefix + bytes(chunk)
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    return qr_codes
