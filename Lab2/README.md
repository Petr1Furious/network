# Lab2

## Реализация скрипта для тестирования MTU в канале

Данный скрипт позволяет найти максимальное значение MTU до указанного адреса. Для этого используется библиотека `pythonping`, значение находится с помощью двоичного поиска до максимально установленной границы (по умолчанию 1500).

Доступные аргументы:
```
usage: main.py [-h] [-i IP] [-x MAX]

options:
  -h, --help         show this help message and exit
  -i IP, --ip IP     Destination IP address
  -x MAX, --max MAX  Max MTU value to check
```

Например, `python3 main.py -i 8.8.8.8 -x 2000`.
