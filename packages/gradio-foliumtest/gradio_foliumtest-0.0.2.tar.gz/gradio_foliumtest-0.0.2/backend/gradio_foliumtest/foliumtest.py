from gradio.components.base import Component
from gradio.data_classes import FileData
from tempfile import NamedTemporaryFile
from folium import Map


class FoliumTest(Component):

    EVENTS = ["change"]

    data_model = FileData

    def __init__(self, value: Map = None, *, height: int = 500, label: str = None):
        super().__init__(value, label=label)
        self.height = height

    def preprocess(self, x):
        return x

    def postprocess(self, x: Map):
        if not x:
            return None

        with NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            x.save(tmp.name)
            return FileData(path=tmp.name, orig_name="map.html")

    def example_inputs(self):
        return {"info": "Do not use as input"}

