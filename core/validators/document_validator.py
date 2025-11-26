from abc import ABC, abstractmethod


class DocumentValidator(ABC):
    @abstractmethod
    def validate(self, document):
        pass


class CPFValidator(DocumentValidator):
    def validate(self, document):
        cleaned_cpf = ''.join(filter(str.isdigit, document))

        if len(cleaned_cpf) != 11:
            return False

        if cleaned_cpf == cleaned_cpf[0] * 11:
            return False

        base_digits = cleaned_cpf[:9]
        total_sum = 0
        for i in range(9):
            total_sum += int(base_digits[i]) * (10 - i)

        remainder = total_sum % 11
        dv1 = 11 - remainder if remainder >= 2 else 0

        base_with_dv1 = base_digits + str(dv1)
        total_sum = 0
        for i in range(10):
            total_sum += int(base_with_dv1[i]) * (11 - i)

        remainder = total_sum % 11
        dv2 = 11 - remainder if remainder >= 2 else 0

        calculated_v_digits = str(dv1) + str(dv2)
        original_v_digits = cleaned_cpf[9:]

        return calculated_v_digits == original_v_digits


class CNPJValidator(DocumentValidator):
    def validate(self, document):
        cleaned_cnpj = ''.join(filter(str.isdigit, document))

        if len(cleaned_cnpj) != 14:
            return False

        if cleaned_cnpj == cleaned_cnpj[0] * 14:
            return False

        base_digits = cleaned_cnpj[:12]
        original_v_digits = cleaned_cnpj[12:]

        def calculate_v_digit(digits_to_check):
            weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            
            start_index = len(weights) - len(digits_to_check) 
            current_weights = weights[start_index:]
            
            total_sum = 0
            for i in range(len(digits_to_check)):
                total_sum += int(digits_to_check[i]) * current_weights[i]

            remainder = total_sum % 11
            
            v_digit = 0 if remainder < 2 else 11 - remainder
            return str(v_digit)

        dv1 = calculate_v_digit(base_digits)

        digits_for_dv2 = base_digits + dv1
        dv2 = calculate_v_digit(digits_for_dv2)

        calculated_v_digits = dv1 + dv2

        return calculated_v_digits == original_v_digits
    

class DocumentValidatorFactory:
    DOCUMENT_TYPES = {
        'CPF': CPFValidator,
        'CNPJ': CNPJValidator,
    }
    
    @staticmethod
    def get_validator(document_type):
        validator_class = DocumentValidatorFactory.DOCUMENT_TYPES.get(document_type)
        if not validator_class:
            raise ValueError(f"Tipo de documento inválido: {document_type}")
        return validator_class()