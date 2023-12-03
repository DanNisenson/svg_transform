import os
from bs4 import BeautifulSoup


def transform():
    has_tried = False

    while True:
        if not has_tried:
            usr_input = input("SVG path: ")
        else:
            usr_input = input("Try again or enter 'q' to quit: ")

        if usr_input == "q":
            print("Quitting...")
            return
        else:
            path = usr_input

        directory, filename = os.path.split(path)

        try:
            with open(path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                break
        except OSError as err:
            print("OS error:", err)
            has_tried = True
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    # find svg
    svgs = soup.find_all("svg")

    for svg in svgs:
        svg["height"], svg["width"] = ["100%", "100%"]

        for child in svgs[0].children:
            if child.name == "path":
                svg["stroke"] = "currentColor"
                svg["fill"] = "none"
                del child["fill"]
                del child["stroke"]
            else:
                svg["fill"] = "currentColor"
                svg["stroke"] = "none"

    new_filename = filename.split(".")[0] + "_ok.svg"
    output_path = os.path.join(directory, new_filename)

    try:
        with open(output_path, "a", encoding="utf-8") as new_file:
            new_file.write(soup.prettify())
    except OSError as err:
        print("OS error:", err)
        has_tried = True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


transform()
