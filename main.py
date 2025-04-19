import argparse
import multiprocessing as mp

from utils import (
    merge_files_metrics,
    reformat_report_for_out,
    print_pretty,
    get_log_numbers_as_dict
)


def process_file(file_name: str, shared_list: list) -> None:
    """Обработка лог файлов"""
    with open(file_name, "r") as file:
        log_numbers = get_log_numbers_as_dict(file)
        shared_list.append(log_numbers)


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


def main():
    with mp.Manager() as manager:
        shared_list = manager.list()
        pool = mp.Pool(mp.cpu_count())
        jobs = []

        for log_file in log_files:
            jobs.append(pool.apply_async(process_file, (log_file, shared_list)))

        for job in jobs:
            job.get()

        pool.close()

        log_numbers_per_file_list = list(shared_list)

    common_file_with_logs_numbers = merge_files_metrics(log_numbers_per_file_list)

    res = reformat_report_for_out(common_file_with_logs_numbers, my_namespace.report)

    total_requests = sum(res[-1][1:-1])

    print(f"Total requests: {total_requests}\n")
    print_pretty(res)


if __name__ == "__main__":
    main()
