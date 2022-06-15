from dash import Dash, html
import dash_cytoscape as cyto

class DashVisualize:
    
    def __init__(self, elements, title):
        app = Dash(__name__)
        app.layout = html.Div([
            html.P(title),
            cyto.Cytoscape(
                id=title,
                elements = elements,
                # elements=[
                #     {'data': {'id': 'ca', 'label': 'Canada'}}, 
                #     {'data': {'id': 'on', 'label': 'Ontario'}}, 
                #     {'data': {'id': 'qc', 'label': 'Quebec'}},
                #     {'data': {'source': 'ca', 'target': 'on'}}, 
                #     {'data': {'source': 'ca', 'target': 'qc'}}
                # ],
                layout={'name': 'breadthfirst'},
                style={'width': '1280px', 'height': '720px'}
            )
        ])

        app.run_server(debug=True)
