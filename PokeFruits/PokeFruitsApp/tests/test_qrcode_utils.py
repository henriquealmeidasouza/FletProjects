import pytest

from qrcode_utils import extract_pokefruit_code


def test_extracts_code_from_pokefruit_json():
    qr_data = '{"name":"Bananachu","code":"5048ba4b0d704e38a4b1b446ad199fd6"}'

    assert extract_pokefruit_code(qr_data) == "5048ba4b0d704e38a4b1b446ad199fd6"


def test_accepts_qr_code_containing_only_the_code():
    assert extract_pokefruit_code("  5048ba4b0d704e38a4b1b446ad199fd6  ") == (
        "5048ba4b0d704e38a4b1b446ad199fd6"
    )


@pytest.mark.parametrize(
    "qr_data",
    ['{"name":"Bananachu"}', '{"code":42}', '{"code":', "[]", ""],
)
def test_rejects_qr_data_without_a_string_code(qr_data):
    with pytest.raises(ValueError):
        extract_pokefruit_code(qr_data)
