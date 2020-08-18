from typing import Callable, List, Union
import datetime


def print_list(term, title: str, items: List[str], selitem: int, page_count: int):
    if selitem > len(items) - 1:
        selitem = len(items) - 1
    elif selitem < 0:
        selitem = 0
    page = selitem // page_count

    output_msgs = [term.center(term.bright_green(title))]
    with term.location(0, 2):
        for i in range(page * page_count, (page + 1) * page_count):
            if i < len(items):
                if i == selitem:
                    output_msgs.append(term.center(term.underline_bright_cyan(f"{i + 1}. {items[i]}")))
                else:
                    output_msgs.append(term.center(f"{i + 1}. {items[i]}"))
        output_msgs.append(term.clear_eos())
        print("\n".join(output_msgs))
    return selitem


def selector(term, title: str, items: List[str], default_selitem: int = 0) -> int:
    selitem = default_selitem
    with term.hidden_cursor(), term.fullscreen():
        while True:
            selitem = print_list(term, title, items, selitem, 30)
            with term.cbreak():
                val = term.inkey(timeout=1)
                if str(val) != "":
                    if str(val) == "q":
                        raise KeyboardInterrupt
                    elif str(val) == "j" or val.name == "KEY_DOWN":
                        selitem += 1
                    elif str(val) == "k" or val.name == "KEY_UP":
                        selitem -= 1
                    elif str(val) == "d":
                        selitem += 30
                    elif str(val) == "u":
                        selitem -= 30
                    elif val.name == "KEY_ENTER":
                        return selitem


default_validator = lambda x: ""


def date_picker(term, prompt: str, default_date: datetime.date,
                validator: Callable[[datetime.date], str] = default_validator) -> datetime.date:
    def validate_date_str(string: str) -> Union[str, datetime.date]:
        try:
            date = datetime.datetime.strptime(string, "%Y-%m-%d").date() if string else default_date
        except ValueError:
            return "Not a valid date."
        return validator(date) or date

    default_date_display = default_date.strftime("%Y-%m-%d")
    disp = f"{prompt} [{default_date_display}]: "
    raw_input = input(disp)
    date_or_error = validate_date_str(raw_input)

    while not isinstance(date_or_error, datetime.date):
        raw_input = input(term.red(f'{disp}({date_or_error}) '))
        date_or_error = validate_date_str(raw_input)

    return date_or_error


def bool_input(term, prompt: str) -> bool:
    disp = f"{prompt} [y/n]: "
    raw_input = input(disp)
    while raw_input not in ["y", "n"]:
        raw_input = input(term.red(disp))
    return raw_input == "y"
