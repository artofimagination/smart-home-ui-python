from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout
)

class LayerControlWidget(QWidget):
    def __init__(self, parent=None):
        super(LayerControlWidget, self).__init__(parent)
        system_layer_button = QPushButton("System")
        heatmap_layer_button = QPushButton("Heatmap")
        light_layer_button = QPushButton("Light")

        # Apply CSS classes to buttons
        system_layer_button.setProperty("class", "system-layer-button")
        heatmap_layer_button.setProperty("class", "heatmap-layer-button")
        light_layer_button.setProperty("class", "light-layer-button")
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(system_layer_button)
        layout.addWidget(heatmap_layer_button)
        layout.addWidget(light_layer_button)