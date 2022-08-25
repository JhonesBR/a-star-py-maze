from threading import Thread
from dash import Dash, html
import dash_cytoscape as cyto
import threading


class DashVisualize:

    def __init__(self, open_list, closed_list, title, port):
        cyto.load_extra_layouts()
        valid_elements = []

        # Create a list of valid elements
        for i in range(len(closed_list)):
            color = "gray"
            if closed_list[i].highlighted:
                color = "red"

            valid_elements.append(
                {
                    "data":
                    {
                        "id": f"[{closed_list[i].position[0]}, {closed_list[i].position[1]}]",
                        "label": f"({i}) f:{closed_list[i].f:.2f} g:{closed_list[i].g} h:{closed_list[i].h:.2f}"
                    },
                    'style':
                    {
                        'background-color': color
                    }
                },
            )
        for i in range(len(open_list)):
            valid_elements.append(
                {
                    "data":
                    {
                        "id": f"[{open_list[i].position[0]}, {open_list[i].position[1]}]",
                        "label": f"({i}) f:{open_list[i].f:.2f} g:{open_list[i].g} h:{open_list[i].h:.2f}"
                    },
                    'style':
                    {
                        'background-color': '#96be25'
                    }
                },
            )

        # Point source -> target on valid_elements
        for node in closed_list:
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
        
        for node in open_list:
            if node.parent:
                valid_elements.append(
                    {
                        "data":
                        {
                            "source": f"[{node.parent.position[0]}, {node.parent.position[1]}]",
                            "target": f"[{node.position[0]}, {node.position[1]}]"
                        },
                        'style':
                        {
                            'line-color': '#96be25'
                        }
                    }
                )


        open_list_positions = [node.position for node in open_list]
        closed_list_positions = [node.position for node in closed_list]
        path = [str(node.position) for node in closed_list if node.highlighted]

        app = Dash(__name__)
        app.layout = html.Div(children=[
            cyto.Cytoscape(
                id=title,
                elements=valid_elements,
                style={'width': '1920px', 'height': '900px'},
                layout={'name': 'dagre'}
            ),
             html.Div(
                children=f'Path: {("-->".join(path))}'
            ),
            html.Div(children='', style={'height': '20px'}),
            html.Div(
                children=f'Open List: {open_list_positions}'
            ),
            html.Div(children='', style={'height': '20px'}),
            html.Div(
                children=f'Closed List: {closed_list_positions}'
            ),
            html.Div(children='', style={'height': '100px'}),
        ])

        threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=port)).start()


class Th(Thread):
    def __init__ (self, open_list, closed_list, title, port):
        self.open_list = open_list
        self.closed_list = closed_list
        self.title = title
        self.port = port
        Thread.__init__(self)

    def run(self):
        DashVisualize(self.open_list, self.closed_list, self.title, self.port)