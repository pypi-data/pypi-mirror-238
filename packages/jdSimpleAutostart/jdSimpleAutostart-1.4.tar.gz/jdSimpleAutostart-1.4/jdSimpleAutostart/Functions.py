import desktop_entry_lib
import os


def is_flatpak() -> bool:
    return os.path.isfile("/.flatpak-info")


def get_system_autostart_path() -> str:
    if is_flatpak():
        return "/run/host/etc/xdg/autostart"
    else:
        return "/etc/xdg/autostart"


def get_user_autostart_path() -> str:
    return os.path.expanduser("~/.config/autostart/")


def generate_desktop_id(name) -> str:
    col = desktop_entry_lib.DesktopEntryCollection()
    col.load_directory(get_system_autostart_path())
    col.load_directory(get_user_autostart_path())

    if name not in col:
        return name

    count = 1
    while True:
        if f"{name}{count}" not in col:
            return f"{name}{count}"
        count += 1


def is_one_in_list(list_a: list, list_b: list) -> bool:
    for i in list_a:
        if i in list_b:
            return True
    return False