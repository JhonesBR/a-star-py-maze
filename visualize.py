from dash import Dash, html
import dash_cytoscape as cyto


class DashVisualize:

    def __init__(self, open_elements, closed_elements, title):
        valid_elements = []

        # Create a list of valid elements
        for i in range(len(closed_elements)):
            valid_elements.append(
                {"data":
                    {"id": i, "label": f"Node {i}"},
                 "position":
                    {"x": closed_elements[i][0]*100,
                        "y": closed_elements[i][1]*100}
                 }
            )

        # Point source -> target on valid_elements
        for i in range(len(closed_elements)-1):
            valid_elements.append({"data": {"source": i, "target": i+1}})

        print(valid_elements)

        app = Dash(__name__)
        app.layout = html.Div(children=[
            cyto.Cytoscape(
                id=title,
                elements=valid_elements,
                style={'width': '1280px', 'height': '720px'},
                layout={'name': 'preset'}
            ), f"Open List: {open_elements}\n\nClosed List: {closed_elements}"
        ])

        app.run_server()
