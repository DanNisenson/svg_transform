import os
import subprocess
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
APP_ICONS_PATH = os.getenv("ICONS_PATH")


def get_path_input(has_tried):
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


def get_component_name():
    usr_input = input("Enter component name in kebab-case: ")

    if has_uppercase(usr_input):
        print("Component name cannot contain uppercase letters")
        return get_component_name()
    else:
        return usr_input


def has_uppercase(input_string):
    return any(char.isupper() for char in input_string)


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


def save_modified_html(soup, component_name, icons_folder):
    full_comp_name = f"{component_name}.component.html"
    component_path = os.path.join(icons_folder, component_name, full_comp_name)

    try:
        with open(component_path, "w", encoding="utf-8") as new_file:
            new_file.write(soup.prettify())
            print(f"Override html at: {component_path}")
    except OSError as err:
        print(f"OS error: {err}")
        return False
    except Exception as err:
        print(f"Unexpected error: {err}")
        raise

    return True


def create_component(component_name):
    proc = subprocess.Popen(
        ["ng", "generate", "component", component_name],
        cwd=APP_ICONS_PATH,
        stdout=subprocess.PIPE,
    )

    print(f"Create component at: {APP_ICONS_PATH}")

    while True:
        line = proc.stdout.readline()
        if not line:
            break


def main():
    has_tried = False

    while True:
        file_path = get_path_input(has_tried)

        if file_path is None:
            return

        html_soup = read_html_file(file_path)

        if not html_soup:
            has_tried = True
            continue
        else:
            break

    component_name = get_component_name()

    if html_soup is not None:
        modify_svg_elements(html_soup)
        create_component(component_name)
        success = save_modified_html(html_soup, component_name, APP_ICONS_PATH)

        if success:
            print("Transformation successful. Modified file saved.")
        else:
            print("Transformation failed.")


if __name__ == "__main__":
    main()
