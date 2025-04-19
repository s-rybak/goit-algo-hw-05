import timeit
from colorama import Fore, Style

# Алгоритм Кнута-Морріса


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# Алгоритм Бойера-Мура


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Бойера-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


text = "Being a developer is not easy"
pattern = "developer"

position = boyer_moore_search(text, pattern)
if position != -1:
    print(f"Substring found at index {position}")
else:
    print("Substring not found")


# Алгоритм Рабіна-Карпа


def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


main_string = "Being a developer is not easy"
substring = "developer"

position = rabin_karp_search(main_string, substring)
if position != -1:
    print(f"Substring found at index {position}")
else:
    print("Substring not found")


# Порівняння алгоритмів

article_1 = open("task3_files/1.txt", "r").read()
article_2 = open("task3_files/2.txt", "r").read()


def test_algorythm_time(algo, text, pattern):
    start_time = timeit.default_timer()
    algo(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time


def test_algorythm(algo):
    return {
        "aritcle_1_success": test_algorythm_time(algo, article_1, "алгоритм"),
        "aritcle_2_success": test_algorythm_time(algo, article_2, "кількість"),
        "aritcle_1_fail": test_algorythm_time(algo, article_1, "ритмічно"),
        "aritcle_2_fail": test_algorythm_time(algo, article_2, "кільку"),
    }


def print_test_result(algo):
    print(f"Алгоритм: {Fore.GREEN}{algo.__name__}{Style.RESET_ALL}")
    res = test_algorythm(algo)
    print(
        f"Статья 1 успішний кейс: {Fore.GREEN}{res['aritcle_1_success']}{Style.RESET_ALL}"
    )
    print(
        f"Статья 2 успішний кейс: {Fore.GREEN}{res['aritcle_2_success']}{Style.RESET_ALL}"
    )
    print(
        f"Статья 1 не успішний кейс: {Fore.RED}{res['aritcle_1_fail']}{Style.RESET_ALL}"
    )
    print(
        f"Статья 2 не успішний кейс: {Fore.RED}{res['aritcle_2_fail']}{Style.RESET_ALL}"
    )


print_test_result(kmp_search)
print_test_result(boyer_moore_search)
print_test_result(rabin_karp_search)
