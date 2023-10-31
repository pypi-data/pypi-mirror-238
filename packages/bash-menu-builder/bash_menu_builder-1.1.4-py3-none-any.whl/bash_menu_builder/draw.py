from .color import Color
import shutil


class Draw:
    @staticmethod
    def separator(symbol: str = '-') -> None:
        columns: int = shutil.get_terminal_size().columns
        print("%s%s" % (Color.ColorOff.value, symbol) * columns)

    @staticmethod
    def paint(string: str) -> str:
        for color in Color:
            string = string.replace("{%s}" % color.name, color.value)

        return string

    @staticmethod
    def count_biggest_line(list_items: list) -> int:
        biggest_line_length: int = 0
        for item in list_items:
            name_length = len(item)
            biggest_line_length = name_length if name_length > biggest_line_length else biggest_line_length

        return biggest_line_length

    @staticmethod
    def add_spaces_for_line_up(line: str, count_biggest_line: int) -> str:
        more_spaces: int = count_biggest_line - len(line)
        return line + ' ' * more_spaces

    @staticmethod
    def get_count_spaces_for_line_up(line: str, count_biggest_line: int) -> int:
        return count_biggest_line - len(line)
