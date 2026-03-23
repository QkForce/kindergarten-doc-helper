from typing import List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class StepIndicator(QWidget):
    def __init__(self, step_labels: List[str], current_step: int = 0):
        super().__init__()
        self.step_labels = step_labels
        self.current_step = current_step
        self.steps = []

        layout = QHBoxLayout(self)
        for i, label in enumerate(step_labels):
            circle = QLabel("●")
            circle.setObjectName("step_indicator_circle")
            indicator_type = (
                "current"
                if i == self.current_step
                else "todo" if i > self.current_step else "done"
            )
            circle.setProperty("indicator-type", indicator_type)

            step_label = QLabel(label)
            step_label.setObjectName("step_indicator_label")
            step_label.setProperty("indicator-type", indicator_type)
            layout.addSpacing(10)
            layout.addWidget(circle)
            layout.addWidget(step_label)

            self.steps.append((circle, step_label))

    def setCurrentStep(self, step_index: int):
        self.current_step = step_index
        for i, (circle, label) in enumerate(self.steps):
            indicator_type = (
                "current"
                if i == self.current_step
                else "todo" if i > self.current_step else "done"
            )
            circle.setProperty("indicator-type", indicator_type)
            circle.style().unpolish(circle)
            circle.style().polish(circle)

            label.setProperty("indicator-type", indicator_type)
            label.style().unpolish(label)
            label.style().polish(label)
