from dash import Dash, html
import dash_cytoscape as cyto
import threading


class DashVisualize:

    def __init__(self, openList, closedList, title,port):
        cyto.load_extra_layouts()
        valid_elements = []

        # Create a list of valid elements
        for i in range(len(closedList)):
            color = "gray"
            if closedList[i].highlighted:
                color = "red"

            valid_elements.append(
                {
                    "data":
                    {
                        "id": f"[{closedList[i].position[0]}, {closedList[i].position[1]}]",
                        "label": f"({i}) f:{closedList[i].f:.2f} g:{closedList[i].g} h:{closedList[i].h:.2f}"
                    },
                    'style':
                    {
                        'background-color': color
                    }
                },
            )

        # Point source -> target on valid_elements
        for node in closedList:
            if node.parent:
                color = "gray"
                if node.highlighted:
                    color = "red"
                valid_elements.append(
                    {
                        "data":
                        {
                            "source": f"[{node.parent.position[0]}, {node.parent.position[1]}]",
                            "target": f"[{node.position[0]}, {node.position[1]}]"
                        },
                        'style':
                        {
                            'line-color': color
                        }
                    }
                )

        app = Dash(__name__)
        app.layout = html.Div(children=[
            cyto.Cytoscape(
                id=title,
                elements=valid_elements,
                style={'width': '1920px', 'height': '1080px'},
                layout={'name': 'dagre'}
            ), f"Open List: {openList}\n\nClosed List: {closedList}"
        ])

        threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=port)).start()
