from .Functions import get_system_autostart_path, get_user_autostart_path
from PyQt6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from .ui_compiled.MainWindow import Ui_MainWindow
from PyQt6.QtCore import Qt, QCoreApplication
from .AddEditDialog import AddEditDialog
from .AddMenuDialog import AddMenuDialog
from PyQt6.QtGui import QIcon
import desktop_entry_lib
import os


class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self, app_icon: QIcon):
        super().__init__()

        self.setupUi(self)

        self._add_menu_dialog = AddMenuDialog(self, app_icon)
        self._add_edit_dialog = AddEditDialog(self)
        self._app_icon = app_icon

        if not self.update_desktop_list():
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Error loading autostart entries"),  QCoreApplication.translate("MainWindow", "One or more autostart entries could not be loaded due to an error. It is possible that these are symbolic links that can cause problems."))

        self.desktop_list.itemChanged.connect(self._item_changed)
        self.desktop_list.itemSelectionChanged.connect(self._update_buttons_enabled)
        self.system_entries_check_box.stateChanged.connect(self.update_desktop_list)
        self.add_button.clicked.connect(self._add_edit_dialog.open_add_dialog)
        self.add_menu_button.clicked.connect(self._add_menu_dialog.open_dialog)
        self.edit_button.clicked.connect(lambda: self._add_edit_dialog.open_edit_dialog(self.desktop_list.currentItem().data(42)))
        self.remove_button.clicked.connect(self._remove_button_clicked)

    def update_desktop_list(self) -> bool:
        col = desktop_entry_lib.DesktopEntryCollection()

        all_ok = True

        if self.system_entries_check_box.isChecked():
            system_path = get_system_autostart_path()
            if os.path.isdir(system_path):
                if not col.load_directory(system_path):
                    all_ok = False

        user_path = get_user_autostart_path()
        if os.path.isdir(user_path):
            if not col.load_directory(user_path):
                all_ok = False

        self.desktop_list.clear()

        for i in col.desktop_entries.values():
            item = QListWidgetItem(i.Name.get_translated_text())

            if i.Hidden:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

            if i.Icon is not None:
                icon = QIcon.fromTheme(i.Icon)
                if icon.isNull():
                    item.setIcon(self._app_icon)
                else:
                    item.setIcon(QIcon.fromTheme(i.Icon))
            else:
                item.setIcon(self._app_icon)

            item.setData(42, i)
            item.setToolTip(i.Comment.get_translated_text())

            self.desktop_list.addItem(item)

        self.desktop_list.sortItems()
        self._update_buttons_enabled()

        return all_ok

    def _item_changed(self, item: QListWidgetItem):
        entry: desktop_entry_lib.DesktopEntry = item.data(42)
        entry.Hidden = item.checkState() == Qt.CheckState.Unchecked
        entry.write_file(os.path.join(get_user_autostart_path(), entry.desktop_id + ".desktop"))

    def _update_buttons_enabled(self):
        if self.desktop_list.currentRow() == -1:
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            return

        self.edit_button.setEnabled(True)

        entry: desktop_entry_lib.DesktopEntry = self.desktop_list.currentItem().data(42)
        self.remove_button.setEnabled(not os.path.exists(os.path.join(get_system_autostart_path(), entry.desktop_id + ".desktop")))

    def _remove_button_clicked(self):
        entry: desktop_entry_lib.DesktopEntry = self.desktop_list.currentItem().data(42)
        os.remove(entry.file_path)
        self.update_desktop_list()
