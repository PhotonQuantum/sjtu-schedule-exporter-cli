import getpass

import blessed
import pysjtu
from pysjtu import Client, JCSSRecognizer, Session
from pysjtu.exceptions import LoginException, OCRException

from . import __version__
from .calendar import schedule_to_ics
from .tui import bool_input, date_picker, selector
from .utils import get_available_filename, get_default_year_term


def banner(term) -> str:
    lines = [f"SJTU Schedule Exporter CLI, Version {__version__}, powered by PySJTU {pysjtu.__version__}",
             f"If you find this tool useful, please star this repo. ",
             f"You are welcomed to submit new issues and PRs if you find any bug in this tool or PySJTU.",
             "",
             f"This project: {term.blue('https://github.com/PhotonQuantum/sjtu-scheudule-exporter-cli')}",
             f"PySJTU: {term.blue('https://github.com/PhotonQuantum/pysjtu')}",
             ""]
    return "\n".join(lines)


def main():
    try:
        sess_file = open("session", mode="r+b")
    except FileNotFoundError:
        sess_file = None

    term = blessed.Terminal()
    print(banner(term))

    print(term.blue("Trying to log into iSJTU..."))
    try:
        with Session(session_file=sess_file, ocr=JCSSRecognizer()) if sess_file else Session(
                ocr=JCSSRecognizer()) as sess:
            if not sess_file:
                username = input("Username: ")
                password = getpass.getpass("Password: ")

                print(term.blue("Logging in..."))
                try:
                    sess.login(username, password)
                except LoginException:
                    print(term.red("Unable to log into iSJTU. Wrong username or password?"))
                except OCRException as e:
                    print(
                        term.red("Failed to solve captcha. Please report the bug and attach the following traceback."))
                    print(str(e))

            client = Client(sess)
            print(term.green(f"Logged in to iSJTU as {client.student_id}."))
            print()

            default_year, default_term = get_default_year_term()
            year_items = list(reversed(range(default_year - 3, default_year + 2)))
            term_items = ["Fall trimester", "Spring trimester", "Summer trimester"]
            year = year_items[selector(term, "Academic year", year_items, 1)]
            print(f"Academic year: {year}")
            trimester = selector(term, "Academic term", term_items, default_term)
            print(f"Academic term: {term_items[trimester]}")
            print()

            print(term.blue("Fetching schedule..."))
            schedule = client.schedule(year, trimester)
            print()

            print(term.green("Just one more step!"))
            validator = lambda date: "A term must start in Monday" if date.weekday() != 0 else date
            default_term_start_date = client.term_start_date
            term_start_date = date_picker(term, "Term start date", default_term_start_date, validator)
            print()

            ics_content = schedule_to_ics(schedule, term_start_date)
            filename = get_available_filename("schedule.ics")
            with open(filename, mode="w") as f:
                f.write(ics_content)

            print(term.green("Done."))
            print()

            if not sess_file:
                save_session = bool_input(term, "Do you want to save your session?")
                if save_session:
                    with open("session", mode="w+b") as f:
                        sess.dump(f)
                    print(term.green(
                        "Saved. You may clear your session at any time by deleting 'session' file in this directory."))
                else:
                    sess.logout()

    except KeyboardInterrupt:
        print(term.red("\nKeyboard interrupted."))


if __name__ == "__main__":
    main()
