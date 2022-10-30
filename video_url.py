def return_url(number, url_answer="video"):
    video_lesson = {
        1: ["Анализ информационных моделей", "https://youtu.be/_9IbqErBWJQ"],
        2: ["Построение таблиц истинности логических выражений", "https://youtu.be/1NGYxJpIG5o"],
        3: ["Поиск информации в реляционных базах данных", "https://youtu.be/xZoC1ME4jIA"],
        4: ["Кодирование и декодирование информации", "К сожалению, я еще не записал видео по этой теме, но оно скоро будет!"],
        5: ["Анализ и построение алгоритмов для исполнителей", "https://youtu.be/FHZ5OVi7T2w"],
        6: ["Анализ программ", "https://youtu.be/99G_ZlyDrww"],
        7: ["Кодирование и декодирование информации. Передача информации", "https://youtu.be/yU9_Ry1jjfA"],
        8: ["Перебор слов и системы счисления", "https://youtu.be/ODICNLimEjA"],
        9: ["Эксель", "https://youtu.be/dgJWnzT_Lb0"],
        10: ["Поиск символов в текстовом редакторе", "https://youtu.be/dMHtI-K1p2Y"],
        11: ["Вычисление количества информации", "https://youtu.be/Av1nCsSzqJI"],
        12: ["Выполнение алгоритмов для исполнителей", "https://youtu.be/PBCJXi8d2os"],
        13: ["Поиск путей в графе", "https://youtu.be/f2EfaScgq34"],
        14: ["Кодирование чисел. Системы счисления", "https://youtu.be/8-eNs6O3VSg"],
        15: ["Преобразование логических выражений", "https://youtu.be/q6XSdMiHyGM"],
        16: ["Рекурсивные алгоритмы", "https://youtu.be/V24gVh_6Cpw"],
        17: ["Обработка целочисленных данных. Проверка делимости", "https://youtu.be/oVptXHQBodI"],
        18: ["Робот-сборщик монет", "https://youtu.be/ytjdtQCg_4k"],
        19: ["Выигрышная стратегия. Задание 1", "https://youtu.be/i297hbGPiUo"],
        20: ["Выигрышная стратегия. Задание 2", "https://youtu.be/i297hbGPiUo"],
        21: ["Выигрышная стратегия. Задание 3", "https://youtu.be/i297hbGPiUo"],
        22: ["Анализ программы с циклами и условными операторами", "https://youtu.be/99G_ZlyDrww"],
        23: ["Оператор присваивания и ветвления. Перебор вариантов, построение дерева", "https://youtu.be/sqndvoUFIjs"],
        24: ["Обработка символьных строк", "https://youtu.be/eQCBq35T3FE"],
        25: ["Обработка целочисленной информации", "https://youtu.be/z1FmHqr8coU"],
        26: ["Обработка целочисленной информации", "https://youtu.be/789EMedzBfY"],
        27: ["Программирование", "https://youtu.be/Q57EVzHby8A"],
    }
    doc_lesson = {
        1: ["Анализ информационных моделей", "https://kpolyakov.spb.ru/download/ege1.doc"],
        2: ["Построение таблиц истинности логических выражений", "https://kpolyakov.spb.ru/download/ege2.doc"],
        3: ["Поиск информации в реляционных базах данных", "https://kpolyakov.spb.ru/download/ege3.doc"],
        4: ["Кодирование и декодирование информации", "https://kpolyakov.spb.ru/download/ege4.doc"],
        5: ["Анализ и построение алгоритмов для исполнителей", "https://kpolyakov.spb.ru/download/ege5.doc"],
        6: ["Выполнение и анализ простых алгоритмов", "https://kpolyakov.spb.ru/download/ege6.doc"],
        7: ["Кодирование и декодирование информации. Передача информации", "https://kpolyakov.spb.ru/download/ege7.doc"],
        8: ["Перебор слов и системы счисления", "https://kpolyakov.spb.ru/download/ege8.doc"],
        9: ["Эксель", "https://kpolyakov.spb.ru/download/ege9.doc"],
        10: ["Поиск символов в текстовом редакторе", "https://kpolyakov.spb.ru/download/ege10.doc"],
        11: ["Вычисление количества информации", "https://kpolyakov.spb.ru/download/ege11.doc"],
        12: ["Выполнение алгоритмов для исполнителей", "https://kpolyakov.spb.ru/download/ege12.doc"],
        13: ["Поиск путей в графе", "https://kpolyakov.spb.ru/download/ege13.doc"],
        14: ["Кодирование чисел. Системы счисления", "https://kpolyakov.spb.ru/download/ege14.doc"],
        15: ["Преобразование логических выражений", "https://kpolyakov.spb.ru/download/ege15.doc"],
        16: ["Рекурсивные алгоритмы", "https://kpolyakov.spb.ru/download/ege16.doc"],
        17: ["Перебор последовательности целых чисел. Проверка делимости", "https://kpolyakov.spb.ru/download/ege17.doc"],
        18: ["Робот-сборщик монет", "https://kpolyakov.spb.ru/download/ege18.doc"],
        19: ["Выигрышная стратегия. Задание 1", "https://kpolyakov.spb.ru/download/ege1921.doc"],
        20: ["Выигрышная стратегия. Задание 2", "https://kpolyakov.spb.ru/download/ege1921.doc"],
        21: ["Выигрышная стратегия. Задание 3", "https://kpolyakov.spb.ru/download/ege1921.doc"],
        22: ["Анализ программы с циклами и условными операторами", "https://kpolyakov.spb.ru/download/ege22.doc"],
        23: ["Оператор присваивания и ветвления. Перебор вариантов, построение дерева", "https://kpolyakov.spb.ru/download/ege23.doc"],
        24: ["Обработка символьных строк", "https://kpolyakov.spb.ru/download/ege24.doc"],
        25: ["Обработка целочисленной информации", "https://kpolyakov.spb.ru/download/ege25.doc"],
        26: ["Обработка целочисленной информации", "https://kpolyakov.spb.ru/download/ege26.doc"],
        27: ["Программирование", "https://kpolyakov.spb.ru/download/ege27.doc"],
    }
    if url_answer == 'video':
        return video_lesson.get(number, 'Неправильный запрос')
    else:
        return doc_lesson.get(number, 'Неправильный запрос')