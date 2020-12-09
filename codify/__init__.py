import qrcode


# TODO: Use Sig to make signatures more DRY

def qr_object(version=None,
              error_correction=0,
              box_size=10,
              border=4,
              image_factory=None,
              mask_pattern=None):
    return qrcode.QRCode(version=version,
                         error_correction=error_correction,
                         box_size=box_size,
                         border=border,
                         image_factory=image_factory,
                         mask_pattern=mask_pattern)


def qrcode_img_of(data,
                  optimize=20,
                  image_factory=None,
                  version=None,
                  error_correction=0,
                  box_size=10,
                  border=4,
                  mask_pattern=None,
                  fill='black',
                  back_color='white',
                  **make_image_kw
                  ):
    q = qr_object(version=version,
                  error_correction=error_correction,
                  box_size=box_size,
                  border=border,
                  image_factory=image_factory,
                  mask_pattern=mask_pattern)
    q.add_data(data, optimize)
    q.make(fit=True)
    return q.make_image(fill=fill, back_color=back_color, **make_image_kw)


import hashlib


def bytes_to_sha256(b: bytes):  # todo: returns string; needs to return bytes
    r"""Compute sha56 of given bytes

    :param b: bytes to compute the sha256 of
    :return: the bytes of the sha256 hash

    >>> bytes_to_sha256(b'bob and alice')
    b'\x0c14\xf2\x834\xa3\xc0\x0c\xe3\xa8i9\r\xe2\xd3\x01\xb1Fj\x11U\x92j^Z\xa8\xaa\x9e\x89\xa2\xd5'

    """
    return hashlib.sha256(b).digest()


def qrcode_img_of_sha256(data, **kwargs):
    if isinstance(data, str):
        data = data.encode()
    assert isinstance(data, bytes), "data needs to be bytes now"
    return qrcode_img_of(bytes_to_sha256(data).hex(), **kwargs)
