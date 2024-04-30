import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, \
    QHBoxLayout, QPushButton, QMessageBox

import StrategyChoice
from CLI.Item_Constructors import generate_item_id
from StrategyChoice import StrategyChoiceField
from SubMenu import InputField, DropDownMenu, tiers, OptionalField, JsonSerializable


# TODO: add tool tips for fields.

def bold_string(text_to_bold):
    return "<b>" + text_to_bold + "</b>"


def underline_string(text_to_underline):
    return "<u>" + text_to_underline + "</u>"


def is_enabled(state):
    if state == 2:
        state.setEnabled(True)
    else:
        state.setEnabled(False)


class ItemCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ore Forge Item Creator")
        # self.setFixedSize(800, 250)
        # self.setWindowIcon(QIcon("icon.png"))
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.essentials_hbox = QHBoxLayout()
        self.generate_button = QPushButton("Generate Item")

        # ComboBox to choose item type
        item_type_label = QLabel(bold_string("Item Type:"))
        # layout.addWidget(self.iem_type_label)
        # self.item_type_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.essentials_hbox.addWidget(item_type_label)

        self.item_type_combo = QComboBox()
        self.item_type_combo.addItem("Dropper")
        self.item_type_combo.addItem("Furnace")
        self.item_type_combo.addItem("Upgrader")
        self.item_type_combo.addItem("Conveyor")
        # layout.addWidget(self.item_type_combo)
        self.essentials_hbox.addWidget(self.item_type_combo, Qt.AlignmentFlag.AlignLeft)

        self.essentials_hbox.addWidget(self.generate_button, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.item_type_combo.currentIndexChanged.connect(self.on_item_type_changed)

        # Print button:

        # Grid layout for item attributes
        self.layout.addLayout(self.essentials_hbox)
        self.essentials_hbox.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.create_common_ui()

        self.generate_button.clicked.connect(
            lambda: self.print_json_data())  #https://stackoverflow.com/questions/40982518/argument-1-has-unexpected-type-nonetype
        self.on_item_type_changed()
        self.show()

    def on_item_type_changed(self):
        text = self.item_type_combo.currentText()
        self.clear_grid_layout()
        self.create_common_ui()
        if text == "Dropper":
            self.create_dropper_ui()
        elif text == "Furnace":
            self.create_furnace_ui()
        elif text == "Upgrader":
            self.create_upgrader_ui()
        elif text == "Conveyor":
            self.create_conveyor_ui()

    def clear_grid_layout(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            self.layout.removeWidget(widget)
            if widget is not None:
                widget.deleteLater()

    def create_common_ui(self):
        self.name = InputField("Name:")
        self.layout.addWidget(self.name)

        self.id = generate_item_id()
        self.id_label = QLabel(bold_string("ID:\t") + self.id)
        self.id_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.id_label)

        self.description = InputField("Description:", 14)
        self.layout.addWidget(self.description)

        self.tier = DropDownMenu(tiers, "Tier:")
        self.layout.addWidget(self.tier)

        self.shopItemField = OptionalField(InputField("Item Price", font_size=14, isInteger=True), "Shop Item")
        self.layout.addWidget(self.shopItemField)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def toggle_price_field(self, state):
        if state == 2:
            self.price_field.setEnabled(True)
        else:
            self.price_field.clear()
            self.price_field.setEnabled(False)

    def create_dropper_ui(self):

        self.oreName = InputField("Ore Name:")
        self.layout.addWidget(self.oreName)

        self.oreValue = InputField("Ore Value:", font_size=14, isInteger=False, isFloat=True)
        self.layout.addWidget(self.oreValue)

        self.oreTemp = InputField("Ore Temp:", font_size=14, isInteger=False, isFloat=True)
        self.layout.addWidget(self.oreTemp)

        self.multiore = InputField("Multiore:", font_size=14, isInteger=True)
        self.layout.addWidget(self.multiore)

        self.dropInterval = InputField("Drop Interval:", font_size=14, isInteger=False, isFloat=True)
        self.layout.addWidget(self.dropInterval)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # oreStrategy

    def create_furnace_ui(self):
        self.pointReward = InputField("Special Point Reward", font_size=14, isInteger=True)
        self.layout.addWidget(self.pointReward)
        self.rewardThreshold = InputField("Special Point Reward Threshold:", font_size=14, isInteger=True)
        self.layout.addWidget(self.rewardThreshold)
        self.strategies = StrategyChoiceField(StrategyChoice.upgradeStrategies)
        self.layout.addWidget(self.strategies)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def create_upgrader_ui(self):
        self.conveyorSpeed = InputField("Conveyor Speed:", font_size=14, isInteger=False, isFloat=True)
        self.maxUpgrades = InputField("Max Upgrades:", font_size=14, isInteger=True)
        self.strategies = StrategyChoiceField(StrategyChoice.upgradeStrategies)
        # self.isResetter = OptionalField()
        self.layout.addWidget(self.conveyorSpeed)
        self.layout.addWidget(self.maxUpgrades)
        self.layout.addWidget(self.strategies)
        # self.layout.addWidget(self.isResetter)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def create_conveyor_ui(self):
        self.conveyorSpeed = InputField("Conveyor Speed:", font_size=14, isInteger=False, isFloat=True)
        self.layout.addWidget(self.conveyorSpeed)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def validate_data(self):
        errorList = []
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, JsonSerializable) and widget.isValid() is not None:
                if isinstance(widget.isValid(), list):
                    errorList.extend(widget.isValid())
                else:
                    errorList.append(widget.isValid())
        return errorList

    def get_data(self):
        errorList = self.validate_data()
        if len(errorList) == 0:
            item_data = {
                "name": self.name.to_json(),
                "id": self.id,
                "description": self.description.to_json(),
                "tier": self.tier.to_json(),
                # "isShopItem": str(self.shop_checkbox.isChecked()).lower() if self.shop_checkbox is not None else "null",
                # "itemValue": int(self.price_field.text()) if (
                #             self.shop_checkbox.isChecked() and self.price_field is not None) else 0
            }
            item_data.update(self.get_item_specific_data())
            return item_data
        else:
            error_box = QMessageBox()
            error_box.setWindowTitle("Validation Error")
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_text = "Data validation failed."
            for error in errorList:
                error_text += "\n" + error
            error_box.setText(error_text)
            error_box.exec()

    def get_item_specific_data(self):
        text = self.item_type_combo.currentText()
        if text == "Dropper":
            return self.get_dropper_data()
        elif text == "Furnace":
            return self.get_furnace_data()
        elif text == "Upgrader":
            return self.get_upgrader_data()
        elif text == "Conveyor":
            return self.get_conveyor_data()
        else:
            return {}

    def get_dropper_data(self):
        dropperData = {
            "blockLayout": [
                [0, 3, 0],
                [0, 0, 0],
                [0, 0, 0],
            ],
            "oreName": self.oreName.to_json(),
            "oreValue": self.oreValue.to_json(),
            "oreTemp": self.oreTemp.to_json(),
            "multiOre": self.multiore.to_json(),
            "dropInterval": self.dropInterval.to_json(),
            # "oreStrategy":
        }
        return dropperData

    def get_furnace_data(self):
        furnaceData = {
            "blockLayout": [
                [4, 4],
                [4, 4],
            ],
            "specialPointReward": self.pointReward.to_json(),
            "rewardThreshold": self.rewardThreshold.to_json(),
            "upgrade": self.strategies.to_json()
        }
        return furnaceData

    def get_upgrader_data(self):
        upgraderData = {
            "blockLayout": [
                [2, 2],
                [1, 1]
            ],
            "conveyorSpeed": self.conveyorSpeed.to_json(),
            "upgrade": self.strategies.to_json(),
            "upgradeTag": {
                "name": self.name.to_json(),
                "id": self.id.to_json(),
                "maxUpgrades": self.maxUpgrades.to_json(),
                # "isResetter": self.isResetter.to_json(),
            }
        }
        return upgraderData

    def get_conveyor_data(self):
        data = {
            "blockLayout": [
                [1, 1],
                [1, 1]
            ],
            "conveyorSpeed": self.conveyorSpeed.to_json()
        }
        return data

    def print_json_data(self):
        data = self.get_data()
        if data is not None:
            json_data = json.dumps(data, indent=4)
            print(json_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ItemCreator()
    win.show()
    sys.exit(app.exec())
