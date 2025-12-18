from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from PySide6.QtWidgets import QVBoxLayout, QWidget

# Matplotlib embedding
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


@dataclass
class ChartPayload:
    kind: str
    data: Dict[str, Any]


class ChartWidget(QWidget):
    """Embedded matplotlib chart.

    kind:
      - mbti_stacked: expects data {"dims": [{name_a,name_b,pct_a,pct_b}, ...]}
      - barh: expects data {"labels": [...], "values": [...]}
    """

    def __init__(self, payload: ChartPayload, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.payload = payload

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.render()

    def render(self) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        kind = self.payload.kind
        data = self.payload.data

        if kind == "mbti_stacked":
            dims: List[Dict[str, Any]] = data.get("dims", [])
            labels = [f"{d['name_a']} vs {d['name_b']}" for d in dims]
            y = list(range(len(dims)))
            for i, d in enumerate(dims):
                ax.barh(i, d["pct_a"], color="#1DB954")
                ax.barh(i, d["pct_b"], left=d["pct_a"], color="#3A3A3A")
                ax.text(d["pct_a"] / 2, i, f"{d['name_a']} {d['pct_a']:.0f}%", ha="center", va="center", color="white", fontsize=9)
                ax.text(d["pct_a"] + d["pct_b"] / 2, i, f"{d['name_b']} {d['pct_b']:.0f}%", ha="center", va="center", color="white", fontsize=9)
            ax.set_xlim(0, 100)
            ax.set_yticks(y)
            ax.set_yticklabels(labels, fontsize=9)
            ax.set_xticks([])
            ax.grid(False)
            ax.set_frame_on(False)
        else:
            labels = data.get("labels", [])
            values = data.get("values", [])
            ax.barh(labels, values, color="#1DB954")
            ax.set_xticks([])
            ax.grid(False)
            ax.set_frame_on(False)

        self.figure.tight_layout()
        self.canvas.draw()
