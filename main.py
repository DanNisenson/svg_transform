import os
from bs4 import BeautifulSoup


def get_user_input(has_tried):
    while True:
        usr_input = input(
            "SVG path: " if not has_tried else "Try again or enter 'q' to quit: "
        )

        if usr_input == "q":
            print("Quitting...")
            return None
        else:
            return usr_input


def read_html_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return BeautifulSoup(file, "html.parser")
    except OSError as err:
        print(f"OS error: {err}")
        return None
    except Exception as err:
        print(f"Unexpected error: {err}")
        raise


def modify_svg_elements(soup):
    svgs = soup.find_all("svg")

    for svg in svgs:
        svg["height"], svg["width"] = ["100%", "100%"]

        for child in svg.children:
            if child.name == "path":
                svg["stroke"] = "currentColor"
                svg["fill"] = "none"
                del child["fill"]
                del child["stroke"]
            else:
                svg["fill"] = "currentColor"
                svg["stroke"] = "none"


def save_modified_html(soup, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as new_file:
            new_file.write(soup.prettify())
    except OSError as err:
        print(f"OS error: {err}")
        return False
    except Exception as err:
        print(f"Unexpected error: {err}")
        raise

    return True


def transform():
    has_tried = False

    while True:
        usr_input = get_user_input(has_tried)

        if usr_input is None:
            return

        directory, filename = os.path.split(usr_input)
        output_filename = filename.split(".")[0] + "_ok.svg"
        output_path = os.path.join(directory, output_filename)

        html_soup = read_html_file(usr_input)

        if not html_soup:
            has_tried = True
            continue
        else:
            break

    if html_soup is not None:
        modify_svg_elements(html_soup)
        success = save_modified_html(html_soup, output_path)

        if success:
            print(f"Transformation successful. Modified file saved at: {output_path}")
        else:
            print("Transformation failed.")


if __name__ == "__main__":
    transform()
