import json


def extract_pokefruit_code(qr_data: str) -> str:
    content = qr_data.strip()
    if not content:
        raise ValueError("O QR Code está vazio.")

    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        if content.startswith(("{", "[")):
            raise ValueError("O QR Code contém um JSON inválido.") from None
        code = content
    else:
        if not isinstance(payload, dict):
            raise ValueError("O QR Code precisa conter um objeto JSON com o campo 'code'.")
        code = payload.get("code")

    if not isinstance(code, str) or not code.strip():
        raise ValueError("O QR Code não contém um código de Pokefruit válido.")

    return code.strip()
