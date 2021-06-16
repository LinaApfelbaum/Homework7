# Homework7

Домашнее задание
Анализ лога веб-сервера

Цель:
Потренироваться писать парсеры для логов.

Написать скрипт анализа приложенного access.log файла
Требования к реализации

Должна быть возможность указать директорию где искать логи или конкретный файл

Должна быть возможность обработки всех логов внутри одной дирректории

Для access.log должна собираться следующая информация:

общее количество выполненных запросов
количество запросов по типу: GET - 20, POST - 10 и т.п.
топ 3 IP адресов, с которых были сделаны запросы
топ 3 самых долгих запросов, должно быть видно метод, url, ip, время запроса
Собранная статистика должна быть сохранена в json файл и выведена в терминал в свободном (но понятном!) формате
Должен быть README.md файл, который описывает как работает скрипт