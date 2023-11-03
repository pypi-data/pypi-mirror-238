from .Functions import get_user_autostart_path, generate_desktop_id
from .ui_compiled.AddEditDialog import Ui_AddEditDialog
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QDialog
import desktop_entry_lib
import os


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class AddEditDialog(QDialog, Ui_AddEditDialog):
    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)

        self.setupUi(self)

        self._current_desktop_entry: Optional[desktop_entry_lib.DesktopEntry] = None
        self._main_window = main_window

        self.button_box.accepted.connect(self._ok_button_clicked)
        self.button_box.rejected.connect(self.close)

    def open_add_dialog(self) -> None:
        self._current_desktop_entry = None

        self.name_edit.setText("")
        self.comment_edit.setText("")
        self.icon_edit.setText("")
        self.exec_edit.setText("")

        self.setWindowTitle(QCoreApplication.translate("AddEditDialog", "Add new autostart entry"))
        self.exec()

    def open_edit_dialog(self, desktop_entry: desktop_entry_lib.DesktopEntry) -> None:
        self._current_desktop_entry = desktop_entry

        self.name_edit.setText(desktop_entry.Name.get_translated_text())
        self.comment_edit.setText(desktop_entry.Comment.get_translated_text())
        self.icon_edit.setText(desktop_entry.Icon or "")
        self.exec_edit.setText(desktop_entry.Exec or "")

        self.setWindowTitle(QCoreApplication.translate("AddEditDialog", "Edit {{Name}}").replace("{{Name}}", desktop_entry.Name.get_translated_text()))
        self.open()

    def _ok_button_clicked(self):
        if self._current_desktop_entry is None:
            entry = desktop_entry_lib.DesktopEntry()
            entry.desktop_id = generate_desktop_id(self.name_edit.text().strip())
        else:
            entry = self._current_desktop_entry

        entry.Name.clear()
        entry.Name.default_text = self.name_edit.text()

        entry.Comment.clear()
        entry.Comment.default_text = self.comment_edit.text()

        if self.icon_edit.text().strip() == "":
            entry.Icon = None
        else:
            entry.Icon = self.icon_edit.text()

        entry.Exec = self.exec_edit.text()

        entry.write_file(os.path.join(get_user_autostart_path(), entry.desktop_id + ".desktop"))

        self._main_window.update_desktop_list()

        self.close()
