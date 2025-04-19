import argparse

from utils import (
    get_handler,
    get_log_level,
    merge_files_metrics,
    reformat_report_for_out,
    print_pretty,
    LOG_LEVELS
)

parser = argparse.ArgumentParser(description='Формирование отчета по данным из указанных лог файлов')
parser.add_argument('log_files', nargs="*", help='лог файлы')
parser.add_argument(
    '--report',
    type=str,
    default="handlers",
    help="имя отчета"
)

my_namespace = parser.parse_args()
log_files = my_namespace.log_files

hand = "django.request"
metrics_per_file_list = []

for log_file in log_files:
    with open(log_file, "r") as file:
        lines = file.readlines()
        log_metrics = {}
        for line in lines:
            line = line.split()
            if line[3].startswith(hand):
                handler = get_handler(line)
                log_level = get_log_level(line)
                handler_dict = log_metrics.setdefault(handler, dict.fromkeys(LOG_LEVELS, 0))
                handler_dict.setdefault(log_level, 0)
                handler_dict[log_level] += 1
        metrics_per_file_list.append(log_metrics)

total_metrics = merge_files_metrics(metrics_per_file_list)

res = reformat_report_for_out(total_metrics, my_namespace.report)

total_requests = sum(res[-1][1:-1])

print(f"Total requests: {total_requests}\n")
print_pretty(res)
