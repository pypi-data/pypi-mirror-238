
# gradio_foliumtest

Create a map with folium and display it on the web with Gradio! 

## Example usage

```python
import gradio as gr
from gradio_foliumtest import FoliumTest
from typing import Literal
from folium import Map


LAT_LONG_MAP = {
    "New York City": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "San Francisco": (37.7749, -122.4194),
    "Tokyo": (35.6762, 139.6503),
    "Miami": (25.7617, -80.1918),
}

def get_city(city: Literal["New York City", "London", "San Francisco", "Tokyo", "Miami"]):
    city = city or "Miami"
    return Map(location=LAT_LONG_MAP[city], zoom_start=12)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            city = gr.Radio(choices=["New York City", "London", "San Francisco", "Tokyo", "Miami"],
                            label="City")
        with gr.Column():
            map_ = FoliumTest(label="Foo")
        city.change(get_city, city, map_)

demo.launch()
```
