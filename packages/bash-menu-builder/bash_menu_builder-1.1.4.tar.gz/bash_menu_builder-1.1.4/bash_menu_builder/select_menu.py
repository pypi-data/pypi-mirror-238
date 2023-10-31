from .abstract_menu import AbstractMenu
from pynput.keyboard import Key, Listener
from .draw import Draw


class SelectMenu(AbstractMenu):
    selected_menu: int = 1

    def show_menu(self) -> None:
        with Listener(on_release=self.__listen_key) as listener:
            self.__draw_menu()
            listener.join()

    def __listen_key(self, key) -> None:
        if key == Key.up:
            self.__pressed_up()

        if key == Key.down:
            self.__pressed_down()

        if key == Key.enter:
            self.__pressed_enter()
            self.__draw_menu(clear_screen=False)

    def __draw_menu(self, clear_screen: bool = True):
        if clear_screen:
            print('\033c')

        if self._banner:
            print(self._banner)

        count: int = 1

        for item in self._menu_items:
            template = '\t\t{Red}[{Yellow}%d{Red}]\t{Cyan} %s'
            if count == self.selected_menu:
                template = '\t\t{BRed}[{BYellow}%d{BRed}] {White}*\t{BCyan} %s'

            print(Draw.paint(template % (
                count,
                item.title
            )))
            count += 1

        print(Draw.paint("\t\t\t {Purple}For {UPurple}Exit{Purple} press {BPurple}Ctrl+C{ColorOff}\n"))

    def __pressed_up(self):
        if self.selected_menu == 1:
            self.selected_menu = len(self._menu_items)
            self.__draw_menu()
            return

        self.selected_menu -= 1
        self.__draw_menu()

    def __pressed_down(self):
        if self.selected_menu == len(self._menu_items):
            self.selected_menu = 1
            self.__draw_menu()
            return

        self.selected_menu += 1
        self.__draw_menu()

    def __pressed_enter(self):
        print('\033c')
        menu_item = self._menu_items[self.selected_menu - 1]
        self._call_handler(menu_item.handler)
