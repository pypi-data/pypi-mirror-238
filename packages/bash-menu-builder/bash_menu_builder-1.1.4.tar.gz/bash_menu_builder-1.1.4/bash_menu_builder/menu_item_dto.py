class MenuItemDto:
    def __init__(
            self,
            title: str,
            handler: object,
            option: str = None,
            short_option: str = None,
            option_value: bool = False
    ):
        self.title: str = title
        self.handler: object = handler
        self.option: str = option.replace(' ', '')
        self.option_value: bool = option_value

        if short_option is not None:
            self.short_option: str = short_option.replace(' ', '')
