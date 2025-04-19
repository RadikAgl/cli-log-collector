""""""
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_handler(line: list) -> str:
    """Извлекает и возвращает url в строковом виде"""
    for elem in line:
        if "/" in elem:
            return elem


def get_log_level(line: list) -> str:
    """Извлекает и возвращает текущий уровень логирования"""
    return line[2]


def merge_files_metrics(metrics_list: list[dict]) -> dict:
    """Возвращает объединенный файл !!!!"""

    metrics_of_all_files = {}
    for file_metrics in metrics_list:
        for key in file_metrics:
            handler_dict = metrics_of_all_files.setdefault(key, dict.fromkeys(LOG_LEVELS, 0))
            for level, number in file_metrics[key].items():
                handler_dict.setdefault(level, 0)
                handler_dict[level] += number

    return metrics_of_all_files


def reformat_report_for_out(report_dict: dict, report_type: str) -> list:
    res = []
    for key in sorted(report_dict.keys()):
        cur_line_elems = [key]
        for level in LOG_LEVELS:
            cur_line_elems.append(report_dict[key][level])

        cur_line_elems.append(sum(cur_line_elems[1:]))
        res.append(cur_line_elems)

    res.insert(0, [report_type.upper(), *LOG_LEVELS, ''])

    t_sum = [0 for _ in range(len(LOG_LEVELS))]
    t_sum.insert(0, '')

    for elem in res[1:]:
        for i in range(1, len(elem) - 1):
            t_sum[i] += elem[i]

    t_sum.append('')
    res.append(t_sum)

    return res


def print_pretty(data: list) -> None:
    """Выводит данные в консоль в табличном виде"""
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(str(max(columns, key=lambda x: len(str(x))))))

    for i, row in enumerate(range(rows)):
        result = []
        for col in range(cols):
            item = str(data[row][col]).ljust(col_width[col])
            result.append(item)

        print('  '.join(result))
