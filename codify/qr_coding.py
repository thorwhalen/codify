"""QR codes"""

import qrcode

from codify.util import bytes_to_sha256

# TODO: Use Sig to make signatures more DRY


def qr_object(
    version=None,
    error_correction=0,
    box_size=10,
    border=4,
    image_factory=None,
    mask_pattern=None,
):
    return qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        image_factory=image_factory,
        mask_pattern=mask_pattern,
    )


def qrcode_img_of(
    data,
    optimize=20,
    image_factory=None,
    version=None,
    error_correction=0,
    box_size=10,
    border=4,
    mask_pattern=None,
    fill="black",
    back_color="white",
    **make_image_kw
):
    q = qr_object(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        image_factory=image_factory,
        mask_pattern=mask_pattern,
    )
    q.add_data(data, optimize)
    q.make(fit=True)
    return q.make_image(fill=fill, back_color=back_color, **make_image_kw)


def qrcode_img_of_sha256(data, **kwargs):
    if isinstance(data, str):
        data = data.encode()
    assert isinstance(data, bytes), "data needs to be bytes now"
    return qrcode_img_of(bytes_to_sha256(data).hex(), **kwargs)
