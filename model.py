import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox,
    QPushButton
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WattsStrogatzApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watts-Strogatz Small-World Generator")
        self._init_ui()

    def _init_ui(self):
        # Central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # Control panel
        ctrl_layout = QHBoxLayout()
        main_layout.addLayout(ctrl_layout)

        # Number of nodes
        ctrl_layout.addWidget(QLabel("Number of nodes (n):"))
        self.nodes_spin = QSpinBox()
        self.nodes_spin.setRange(10, 1000)
        self.nodes_spin.setValue(100)
        ctrl_layout.addWidget(self.nodes_spin)

        # Average degree k
        ctrl_layout.addWidget(QLabel("Average degree (k):"))
        self.k_spin = QSpinBox()
        self.k_spin.setRange(2, 50)
        self.k_spin.setSingleStep(2)
        self.k_spin.setValue(4)
        ctrl_layout.addWidget(self.k_spin)

        # Rewiring probability beta
        ctrl_layout.addWidget(QLabel("Rewiring probability (beta):"))
        self.beta_spin = QDoubleSpinBox()
        self.beta_spin.setRange(0.0, 1.0)
        self.beta_spin.setSingleStep(0.01)
        self.beta_spin.setValue(0.1)
        ctrl_layout.addWidget(self.beta_spin)

        # Generate button
        self.gen_button = QPushButton("Generate Network")
        self.gen_button.clicked.connect(self.generate_network)
        ctrl_layout.addWidget(self.gen_button)

        # Matplotlib canvas
        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

    def generate_network(self):
        # Read parameters
        n = self.nodes_spin.value()
        k = self.k_spin.value()
        p = self.beta_spin.value()

        # Generate network
        G = nx.watts_strogatz_graph(n, k, p)

        # Draw network
        self.ax.clear()
        pos = nx.circular_layout(G)
        nx.draw(G, pos, ax=self.ax, node_size=50)
        self.ax.set_title(f"Watts-Strogatz Graph (n={n}, k={k}, \u03B2={p})")
        self.ax.axis('off')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WattsStrogatzApp()
    window.show()
    sys.exit(app.exec_())
