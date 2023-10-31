from .color import Color
from .draw import Draw
from .abstract_menu import AbstractMenu


class InputMenu(AbstractMenu):
    def show_menu(self) -> None:
        if self._banner:
            print(self._banner)

        self.__draw_menu()

    def __draw_menu(self) -> None:
        print(Color.ColorOff.value)
        count: int = 1
        for item in self._menu_items:
            print(Draw.paint("\t\t{Red}[{Yellow}%d{Red}]\t{Cyan} %s" % (count, item.title)))
            count += 1

        print(Draw.paint("\t\t\t {Purple}For {UPurple}Exit{Purple} press {BPurple}Ctrl+C{ColorOff}\n"))
        self.__propose_choose()

    def __propose_choose(self) -> None:
        try:
            selected_menu = int(input(Draw.paint("\t\t{Green}Choose menu number {ColorOff}>> "))) - 1
            menu_item = self._menu_items[selected_menu]
            self._call_handler(menu_item.handler)
            self.__draw_menu()

        except (RuntimeError, ValueError, KeyboardInterrupt, IndexError):
            print(Draw.paint('\t\t{BRed}Error: {Red} Incorrect selected menu!{ColorOff}\n'))
            self.__propose_choose()
