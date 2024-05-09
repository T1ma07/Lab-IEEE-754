# Функція для представлення числа у форматі ЧПТ
def float_to_binary(num, char_size, mantissa_size):
    # Розбиваємо число на знак, мантису та експоненту
    sign = '0' if num >= 0 else '1'
    num = abs(num)
    exponent = 0
    while num >= 2:
        num /= 2
        exponent += 1
    mantissa = num - 1  # Вираховуємо мантису для нормалізованого ЧПТ

    # Перевіряємо, чи маємо нормалізоване представлення
    if exponent >= -1 and exponent <= ((1 << (char_size - 1)) - 2):
        # Нормалізоване представлення
        exponent_bits = bin(exponent + ((1 << (char_size - 1)) - 1))[2:].zfill(char_size)
        mantissa_bits = format(int(mantissa * (1 << mantissa_size)), '0{}b'.format(mantissa_size))
    else:
        # Ненормалізоване представлення
        exponent_bits = '0' * char_size
        mantissa_bits = format(int(num * (1 << mantissa_size)), '0{}b'.format(mantissa_size))
        if exponent == -1:
            exponent_bits = '0' * char_size
            mantissa_bits = '0' * mantissa_size

    return sign, exponent_bits, mantissa_bits

# Функція для виведення ЧПТ у зручному форматі
def print_float_binary(sign, exponent_bits, mantissa_bits):
    print("Sign:       ", sign)
    print("Exponent:   ", exponent_bits)
    print("Mantissa:   ", mantissa_bits)

def binary_to_decimal(binary_str):
    decimal = 0
    for digit in binary_str:
        # Якщо розряд від'ємний, ігноруємо його
        if digit == '-':
            continue
        decimal = decimal * 2 + int(digit)
    return decimal


# Стандартні представлення ЧПТ
standard_floats = [
    0.0,                    # Мінімальне за абсолютною величиною ненульове представлення
    float('+inf'),          # Максимальне додатнє представлення
    float('-inf'),          # Мінімальне від’ємне представлення
    1.0,                    # Число +1,0Е0
    float('+inf'),          # Значення +∞
    float('-inf'),          # Значення -∞
    0.1,                    # Ненормалізоване представлення
    float('nan')            # NaN-значення
]

# Введення ЧПТ користувачем
user_input = input("Enter a floating point number in the format ±x.x...xE±x...x: ")

# Розділення введеного значення на мантису та експоненту
parts = user_input.split('E')

# Перевірка чи введено правильне значення
if len(parts) == 2:
    mantissa_part = parts[0].replace('.', '')
    exponent_part = parts[1].replace('+', '')
    sign = '1' if user_input[0] == '-' else '0'
    # Формування бітового представлення
    exponent_bits = exponent_part.zfill(8)
    mantissa_bits = ''.join(['1' if bit == '-' else bit for bit in mantissa_part])[:16]

    print("\nUser Input Binary Representation:")
    print_float_binary(sign, exponent_bits, mantissa_bits)

    # Конвертація ЧПТ у десяткове число та виведення результату без використання binary_to_float
    sign_multiplier = -1 if sign == '1' else 1
    # Перевірка на від'ємний експонент
    if exponent_bits[0] == '1':
        # Обчислення від'ємного значення експоненти
        exponent = -binary_to_decimal(exponent_bits[1:])
    else:
        # Позитивний експонент, просто конвертуємо в десяткове число
        exponent = binary_to_decimal(exponent_bits)
    mantissa = sign_multiplier * (1 + sum(int(bit) * 2 ** -(i + 1) for i, bit in enumerate(mantissa_bits)))
    converted_num = mantissa * 2 ** exponent
    print("\nConverted to Decimal:", converted_num)
else:
    print("Invalid input format. Please enter the number in the correct format.")


# Виведення стандартних представлень ЧПТ
print("Standard Float Representations:")
for num in standard_floats:
    binary_representation = float_to_binary(num, 8, 16)
    print("Decimal:", num)
    print("Binary: ", binary_representation)
    print("")
