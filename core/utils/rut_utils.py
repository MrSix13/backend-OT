import re

def validar_rut(rut):
    rut = rut.replace('.', '').replace('-', '').upper()

    # Verificar el formato del Rut con expresión regular
    pattern = re.compile(r"^\d{1,8}-[0-9K]$")
    if not pattern.match(rut):
        return False

    # Separar el número y el dígito verificador
    num, dv = rut.split('-')

    # Verificar dígito verificador
    total = 0
    factor = 2
    for d in reversed(num):
        total += int(d) * factor
        factor = 2 if factor == 7 else factor + 1

    expected_dv = str(11 - (total % 11))
    if expected_dv == '10':
        expected_dv = 'K'
    elif expected_dv == '11':
        expected_dv = '0'

    return dv == expected_dv
