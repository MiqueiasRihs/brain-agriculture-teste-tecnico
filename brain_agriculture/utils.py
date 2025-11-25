from django.core.exceptions import ValidationError

def validate_cpf_cnpj(value):
    num = ''.join(filter(str.isdigit, value))

    if len(num) == 11:
        return num

    elif len(num) == 14:
        return num

    raise ValidationError("CPF ou CNPJ inválido. Deve conter 11 (CPF) ou 14 (CNPJ) dígitos.")