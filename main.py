import argparse
from datetime import datetime


def get_current_time() -> str:
    """Возвращает текущее дата-время в строковом виде"""
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")


parser = argparse.ArgumentParser(description='Формирование отчета на основе предоставленных лог файлов')
parser.add_argument('log_files', nargs="*", help='лог файлы')
parser.add_argument(
    '--report',
    type=str,
    default=f"handlers_{get_current_time()}",
    help="имя файла отчета"
)
my_namespace = parser.parse_args()
print(my_namespace.report)
print(my_namespace.log_files)
