import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox,
    QPushButton, QSizePolicy, QSplitter
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WattsStrogatzApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watts-Strogatz Small-World Generator")
        self._init_ui()
        self.resize(1200, 600)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout splitter (controls vs canvas)
        splitter = QSplitter(Qt.Vertical)
        layout = QVBoxLayout(central)
        layout.addWidget(splitter)

        # Top: control panel
        ctrl_widget = QWidget()
        ctrl_layout = QHBoxLayout(ctrl_widget)
        splitter.addWidget(ctrl_widget)

        # Controls
        for label_text, widget in [
            ("Nodes (n):", QSpinBox()),
            ("Degree (k):", QSpinBox()),
            ("Beta (p):", QDoubleSpinBox())
        ]:
            ctrl_layout.addWidget(QLabel(label_text))
            widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            ctrl_layout.addWidget(widget)
            if label_text.startswith("Nodes"):
                self.nodes_spin = widget; self.nodes_spin.setRange(10, 1000); self.nodes_spin.setValue(100)
            elif label_text.startswith("Degree"):
                self.k_spin = widget; self.k_spin.setRange(2, 50); self.k_spin.setSingleStep(2); self.k_spin.setValue(4)
            else:
                self.beta_spin = widget; self.beta_spin.setRange(0.0, 1.0); self.beta_spin.setSingleStep(0.01); self.beta_spin.setValue(0.1)

        # Generate button
        self.gen_button = QPushButton("Generate Network")
        self.gen_button.clicked.connect(self.generate_network)
        ctrl_layout.addWidget(self.gen_button)

        # Metrics display in a dedicated sub-layout
        metrics_widget = QWidget()
        metrics_layout = QHBoxLayout(metrics_widget)
        splitter.addWidget(metrics_widget)
        self.clustering_label = QLabel("Clustering: N/A")
        self.distance_label = QLabel("Avg Path: N/A")
        for lbl in (self.clustering_label, self.distance_label):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            metrics_layout.addWidget(lbl)

        # Bottom: plotting area
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        splitter.addWidget(plot_widget)
        self.figure, self.axes = plt.subplots(1, 3)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_layout.addWidget(self.canvas)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 0)
        splitter.setStretchFactor(2, 1)

    def generate_network(self):
        n, k, p = self.nodes_spin.value(), self.k_spin.value(), self.beta_spin.value()
        G = nx.watts_strogatz_graph(n, k, p)
        clustering = nx.average_clustering(G)
        try:
            avg_distance = nx.average_shortest_path_length(G)
        except nx.NetworkXError:
            comp = max(nx.connected_components(G), key=len)
            avg_distance = nx.average_shortest_path_length(G.subgraph(comp))
        self.clustering_label.setText(f"Clustering: {clustering:.4f}")
        self.distance_label.setText(f"Avg Path: {avg_distance:.4f}")

        pos = nx.circular_layout(G)
        for ax in self.axes: ax.clear()
        nx.draw(G, pos, ax=self.axes[0], node_size=30)
        self.axes[0].set_title("Graph"); self.axes[0].axis('off')
        degrees = [d for _, d in G.degree()]
        self.axes[1].hist(degrees, bins=range(min(degrees), max(degrees)+2), align='left', edgecolor='black')
        self.axes[1].set_title("Degree Dist."); self.axes[1].set_xlabel("k"); self.axes[1].set_ylabel("Count")
        distances = [np.hypot(pos[u][0]-pos[v][0], pos[u][1]-pos[v][1]) for u,v in G.edges()]
        self.axes[2].hist(distances, bins=20, edgecolor='black')
        self.axes[2].set_title("Link Dist."); self.axes[2].set_xlabel("Euclidean"); self.axes[2].set_ylabel("Count")

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WattsStrogatzApp()
    window.show()
    sys.exit(app.exec_())
