from enum import Enum


class Runtime(str, Enum):
    FLIGHT = "flight"
    MLFLOW = "mlflow"
    ONNX = "onnx"
    PYTHON = "python"
    TENSORFLOW = "tensorflow"

    def __str__(self) -> str:
        return str(self.value)
