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
        mantissa_bits = format(int(mantissa * (1 << mantissa_size)), '0{}b'.format(mantissa_size))

    return sign, exponent_bits, mantissa_bits

# Функція для виведення ЧПТ у зручному форматі
def print_float_binary(sign, exponent_bits, mantissa_bits):
    print("Sign:       ", sign)
    print("Exponent:   ", exponent_bits)
    print("Mantissa:   ", mantissa_bits)

# Функція для конвертації ЧПТ у десяткове число
def binary_to_float(sign, exponent_bits, mantissa_bits):
    sign = -1 if sign == '1' else 1
    exponent = int(exponent_bits, 2) - ((1 << (len(exponent_bits) - 1)) - 1)
    mantissa = 1 + sum([int(bit) * 2 ** -(i + 1) for i, bit in enumerate(mantissa_bits)])
    return sign * mantissa * 2 ** exponent

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

# Виведення стандартних представлень ЧПТ
print("Standard Float Representations:")
for num in standard_floats:
    binary_representation = float_to_binary(num, 8, 16)
    print("Decimal:", num)
    print("Binary: ", binary_representation)
    print("")

# Введення ЧПТ користувачем
user_input = input("Enter a floating point number in the format ±x.x...xE±x...x: ")
# Розділення введеного значення на мантису та експоненту
parts = user_input.split('E')
mantissa_part = parts[0].replace('.', '')
exponent_part = parts[1].replace('+', '')
sign = '1' if user_input[0] == '-' else '0'
# Формування бітового представлення
exponent_bits = bin(int(exponent_part))[2:].zfill(8)
mantissa_bits = ''.join(['1'] + [bit for bit in mantissa_part])[:16]

print("\nUser Input Binary Representation:")
print_float_binary(sign, exponent_bits, mantissa_bits)

# Конвертація ЧПТ у десяткове число та виведення результату
converted_num = binary_to_float(sign, exponent_bits, mantissa_bits)
print("\nConverted to Decimal:", converted_num)
