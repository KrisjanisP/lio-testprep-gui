from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from datetime import datetime

class ReloadLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Last reloaded: Never")

    def update_reload_label(self):
        now = datetime.now()
        lastReloadedText = now.strftime("Last reloaded: %Y-%m-%d %H:%M:%S")
        self.setText(lastReloadedText)
    
class ReloadLabelRow(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.reloadLabel = ReloadLabel()
        self.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.addWidget(self.reloadLabel)
    def update_reload_label(self):
        self.reloadLabel.update_reload_label()