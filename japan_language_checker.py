import re


def contains_latin_letters(text):
    """
    Проверяет, содержит ли текст латинские буквы (A-Z, a-z)
    включая одиночные буквы
    """
    # Регулярное выражение для любой латинской буквы
    return bool(re.search(r'[A-Za-z]', text))


def filter_out_latin(input_path, output_path):
    """
    Удаляет строки с любыми латинскими буквами
    """
    pure_japanese_lines = []
    removed_lines = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            if contains_latin_letters(line):
                removed_lines.append((line_num, line))
            else:
                pure_japanese_lines.append(line)

    # Сохраняем чистые японские строки
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in pure_japanese_lines:
            f.write(f"{line}\n")

    # Сохраняем лог удалённых строк
    if removed_lines:
        log_path = output_path.replace('.txt', '_removed_latin.log')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"Удалено строк с латинскими буквами: {len(removed_lines)}\n")
            f.write("=" * 60 + "\n")
            for line_num, text in removed_lines[:100]:  # Первые 100 примеров
                f.write(f"Строка {line_num}: {text}\n")

    print(f"Результаты фильтрации:")
    print(f"Исходно строк: {len(pure_japanese_lines) + len(removed_lines)}")
    print(f"Чистых японских строк (без латиницы): {len(pure_japanese_lines)}")
    print(f"Удалено строк с латиницей: {len(removed_lines)}")

    if removed_lines:
        print(f"\nПримеры удалённых строк:")
        for line_num, text in removed_lines[:5]:
            print(f"  Строка {line_num}: {text[:80]}...")

    return pure_japanese_lines


# ДОПОЛНИТЕЛЬНАЯ ФУНКЦИЯ: Удаление римских цифр (I, V, X, L, C, D, M)
def contains_roman_numerals(text):
    """
    Проверяет наличие римских цифр
    """
    return bool(re.search(r'\b[IVXLCDM]+\b', text, re.IGNORECASE))


def filter_strict_japanese(input_path, output_path):
    """
    Строгая фильтрация: удаляет строки с:
    1. Латинскими буквами (A-Z, a-z)
    2. Римскими цифрами
    3. Латинскими словами в кавычках (например "Protego")
    """
    pure_japanese_lines = []
    removed_by_latin = []
    removed_by_roman = []
    removed_by_quotes = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            # 1. Проверка на латинские буквы
            if re.search(r'[A-Za-z]', line):
                removed_by_latin.append((line_num, line))
                continue

            # 2. Проверка на римские цифры
            if re.search(r'\b[IVXLCDM]+\b', line, re.IGNORECASE):
                removed_by_roman.append((line_num, line))
                continue

            # 3. Проверка на латинские слова в кавычках (например “Protego”)
            # Ищем последовательности латинских букв в японских/английских кавычках
            if re.search(r'[「」『』"\'][A-Za-z]+[「」『』"\']', line):
                removed_by_quotes.append((line_num, line))
                continue

            pure_japanese_lines.append(line)

    # Сохраняем
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in pure_japanese_lines:
            f.write(f"{line}\n")

    # Сохраняем детальный лог
    total_removed = len(removed_by_latin) + len(removed_by_roman) + len(removed_by_quotes)
    if total_removed > 0:
        log_path = output_path.replace('.txt', '_strict_filter.log')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"ДЕТАЛЬНАЯ СТАТИСТИКА ФИЛЬТРАЦИИ\n")
            f.write("=" * 60 + "\n")
            f.write(f"Исходно строк: {len(pure_japanese_lines) + total_removed}\n")
            f.write(f"Сохранено строк: {len(pure_japanese_lines)}\n")
            f.write(f"Всего удалено: {total_removed}\n\n")

            f.write(f"Удалено по категориям:\n")
            f.write(f"  1. Латинские буквы: {len(removed_by_latin)}\n")
            f.write(f"  2. Римские цифры: {len(removed_by_roman)}\n")
            f.write(f"  3. Латинские слова в кавычках: {len(removed_by_quotes)}\n\n")

            if removed_by_latin:
                f.write("Примеры удалённых (латинские буквы):\n")
                for line_num, text in removed_by_latin[:10]:
                    f.write(f"  Строка {line_num}: {text}\n")
                f.write("\n")

            if removed_by_roman:
                f.write("Примеры удалённых (римские цифры):\n")
                for line_num, text in removed_by_roman[:5]:
                    f.write(f"  Строка {line_num}: {text}\n")
                f.write("\n")

            if removed_by_quotes:
                f.write("Примеры удалённых (слова в кавычках):\n")
                for line_num, text in removed_by_quotes[:5]:
                    f.write(f"  Строка {line_num}: {text}\n")

    print(f"\nСТРОГАЯ ФИЛЬТРАЦИЯ ЗАВЕРШЕНА:")
    print(f"Сохранено чистых японских строк: {len(pure_japanese_lines)}")
    print(f"Удалено: {total_removed} строк")
    print(f"  - Латинские буквы: {len(removed_by_latin)}")
    print(f"  - Римские цифры: {len(removed_by_roman)}")
    print(f"  - Слова в кавычках: {len(removed_by_quotes)}")

    return pure_japanese_lines


# БЫСТРЫЙ ВАРИАНТ: Если нужна только основная фильтрация
def quick_filter_japanese(input_path, output_path):
    """
    Быстрая фильтрация латиницы (основные проблемы из ваших примеров)
    """
    pattern = re.compile(r'[A-Za-z]')  # Любая латинская буква

    with open(input_path, 'r', encoding='utf-8') as f_in:
        lines = [line.strip() for line in f_in if line.strip()]

    filtered = [line for line in lines if not pattern.search(line)]

    with open(output_path, 'w', encoding='utf-8') as f_out:
        for line in filtered:
            f_out.write(f"{line}\n")

    print(f"Быстрая фильтрация:")
    print(f"Исходно: {len(lines)} строк")
    print(f"После фильтрации: {len(filtered)} строк")
    print(f"Удалено: {len(lines) - len(filtered)} строк")

    return filtered


# Использование:
if __name__ == "__main__":
    input_file = "book_japanese/parsed_sentences/japanese_final_unique.txt"

    # Вариант 1: Быстрая фильтрация
    output_file1 = "book_japanese/parsed_sentences/japanese_no_latin.txt"
    print("=" * 60)
    print("БЫСТРАЯ ФИЛЬТРАЦИЯ (удаление латинских букв)")
    print("=" * 60)
    filtered1 = quick_filter_japanese(input_file, output_file1)

    # Вариант 2: Строгая фильтрация
    output_file2 = "book_japanese/parsed_sentences/japanese_pure_strict.txt"
    print("\n" + "=" * 60)
    print("СТРОГАЯ ФИЛЬТРАЦИЯ")
    print("=" * 60)
    filtered2 = filter_strict_japanese(input_file, output_file2)

    # Вывод примеров
    print("\n" + "=" * 60)
    print("ПЕРВЫЕ 10 ОТФИЛЬТРОВАННЫХ ПРЕДЛОЖЕНИЙ:")
    print("=" * 60)
    for i, sent in enumerate(filtered2[:10]):
        print(f"{i + 1}: {sent}")

    # Проверка что не осталось латиницы
    print("\n" + "=" * 60)
    print("ПРОВЕРКА НА НАЛИЧИЕ ЛАТИНИЦЫ:")
    print("=" * 60)

    latin_found = False
    for i, sent in enumerate(filtered2[:100]):  # Проверяем первые 100
        if re.search(r'[A-Za-z]', sent):
            print(f"НАЙДЕНО в строке {i + 1}: {sent[:50]}...")
            latin_found = True

    if not latin_found:
        print("✓ Латинских букв не обнаружено!")