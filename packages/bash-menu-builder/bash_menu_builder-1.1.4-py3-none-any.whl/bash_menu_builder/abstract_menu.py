from abc import ABC, abstractmethod
from .menu_item_dto import MenuItemDto
import signal
import sys


class AbstractMenu(ABC):
    def __init__(self, menu: list[MenuItemDto], banner: str = None) -> None:
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        self._menu_items = menu
        self._banner = banner
        self.__check_options()
        self.show_menu()

    def __check_options(self):
        if '--help' in sys.argv:
            for menu_item in self._menu_items:
                option = '--%s' % menu_item.option
                print('\t%s\t\t - %s' % (option, menu_item.title))
            exit()

        for menu_item in self._menu_items:
            option = '--%s' % menu_item.option
            if option in sys.argv:
                self._call_handler(menu_item.handler)
                exit()

    @staticmethod
    def _call_handler(handler) -> None:
        if not callable(handler):
            raise RuntimeError('Item has incorrect Callable type!')

        handler()

    @abstractmethod
    def show_menu(self) -> None:
        pass
