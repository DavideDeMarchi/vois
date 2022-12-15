"""SVG visualization of a graph."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2023
# 
# Licensed under the EUPL, Version 1.2 or as soon they will be approved by 
# the European Commission subsequent versions of the EUPL (the "Licence");
# 
# You may not use this work except in compliance with the Licence.
# 
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS"
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# 
# See the Licence for the specific language governing permissions and
# limitations under the Licence.
from ipywidgets import HTML, widgets, Layout
from ipyevents import Event
from IPython.display import display
import math
from textwrap import wrap

try:
    from . import colors
    from .vuetify import fontsettings
    from .vuetify import settings
except:
    import colors
    from vuetify import fontsettings
    from vuetify import settings


###########################################################################################################################################################################
# Visualization of a Graph with predefined positions
###########################################################################################################################################################################
def svgGraph(nodes_name,
             nodes_label,
             nodes_color,
             nodes_pos,
             edges,
             edge_label='Value',
             textcolor='white',
             edgestrokecolor='lightgrey',
             edgestrokewidth=0.3,
             nodestrokecolor='grey',
             nodestrokewidth=0.3,
             selectedcolor='red',
             selectedstrokewidth=0.7,
             width=300.0,
             heightpercent=100.0,
             borderspercent=10.0,
             nodesradius=3.0,
             fontsize=3.0,
             onclick=None):
    """
    Display of a graph.
    
    Parameters
    ----------
    nodes_name : dict
        Dictionary with Key=nodeid and Value=name (short label to display inside the node)
    nodes_label : dict
        Dictionary with Key=nodeid and Value=description (long description to display as tooltip of the nodes)
    nodes_color : dict
        Dictionary with Key=nodeid and Value=color to use for the node
    nodes_pos : dict
        Dictionary with Key=nodeid and Value=[x,y] coordinates of the node
    edges : dict
        Dictionary with Key=(nodeid1,nodeid2) and Value containing a numerical value to display in the tooltip
    edge_label : str, optional
        String to display inside the tooltip over an edge of the graph (default is 'Value')
    textcolor : str, optional
        Color to use for text of nodes (default is 'white')
    edgestrokecolor : str, optional
        Color to use to display the edges (default is 'lightgrey')
    edgestrokewidth : float, optional
        Stroke width of the line used to display the edges (default is 0.3)
    nodestrokecolor : str, optional
        Color to use for the border of the nodes (default is 'grey')
    nodestrokewidth : float, optional
        Stroke width of the line used to display the border of the nodes (default is 0.3)
    selectedcolor : str, optional
        Color to use to display the border of the selected node (default is 'red')
    selectedstrokewidth : float, optional
        Stroke width of the line used to display the border of the selected node (default is 0.7)
    width : int or float or str, optional
        Width of the drawing. If an integer or a float is passed, the size is intended in pixels units, otherwise a string containing the units must be passed (example: '4vw'). The default is 300.0 for 300 pixels
    heightpercent : float, optional
        Height of the drawing in percentage of the Width (default is 100.0, meaning that a square chart will be created)
    borderspercent : float, optional
        Border to add in percentage on each side of the chart to be sure that the nodes circles are completely inside (default is 10.0)
    nodesradius : float, optional
        Radius of the circles that represent the nodes. The total graph drawing is created in SVG coordinates [0,100]. Default is 3.0.
    fontsize : float, optional
        Size of the font used for nodes' texts. The total graph drawing is created in SVG coordinates [0,100]. Default is 3.0.
    onclick : function, optional
        Python function to call when the user clicks on one of the nodes of the graph. The function will receive as parameter the nodeid of the clicked node, or -1 when the click is outside of all the nodes
        
    Returns
    -------
        an ipywidgets.Output instance with the graph displayed inside
        
    Example
    -------
    Example of a generation and display of a random graph using networkx library and svgGraph module::
    
        from vois import svgGraph
        import networkx as nx
        import random
        r = lambda: random.randint(0,255)

        # Generate a random graph using networkx
        G = nx.gnp_random_graph(20, 0.2, seed=12345)
        
        # Assign position to nodes using Fruchterman-Reingold force-directed algorithm
        nodes_pos = nx.spring_layout(G, weight='weight', seed=12345)

        # Extract nodes and edges information from the graph
        nodes = list(G.nodes)
        edges = list(G.edges)
        
        # Generate dictionaries requested by the svgGraph module
        nodes_name  = dict(zip(nodes,['N'+str(x) for x in nodes]))
        nodes_label = dict(zip(nodes,['Description of node '+str(x) for x in nodes]))
        nodes_color = dict(zip(nodes,['#%02X%02X%02X' % (r(),r(),r()) for x in nodes]))  # Random colors

        edges_value = dict(zip(edges,[random.randint(0,100) for x in edges]))

        # Display the graph
        svgGraph.svgGraph(nodes_name, nodes_label, nodes_color, nodes_pos, edges_value, width=800)

    .. figure:: figures/graph.png
       :scale: 100 %
       :alt: Graph example

       Example of a graph visualization
    
    """
    
    # Calculate bounding box
    xmin = ymin =  1.0e+300
    xmax = ymax = -1.0e+300
    for node, coords in nodes_pos.items():
        x = coords[0]
        y = coords[1]
        if x < xmin: xmin = x
        if x > xmax: xmax = x
        if y < ymin: ymin = y
        if y > ymax: ymax = y
    
    dx = xmax - xmin
    dy = ymax - ymin
    
    # If the height is bigger than requested
    opimaldy = dx * heightpercent / 100.0
    if dy != opimaldy:
        ymin =  1.0e+300
        ymax = -1.0e+300
        f = opimaldy/dy
        for node, coords in nodes_pos.items():
            coords[1] *= f
            if coords[1] < ymin: ymin = coords[1]
            if coords[1] > ymax: ymax = coords[1]
        

    # Enlarge on each side
    enlarge = borderspercent / 100.0
    xmin -= enlarge*dx
    xmax += enlarge*dx
    ymin -= enlarge*dy
    ymax += enlarge*dy
    
    dx = xmax - xmin
    dy = ymax - ymin
    height = 100.0 * dy / dx
    
    radiussvg = nodesradius   # Circles radius in SVG coordinates

    # Convert coordinates to [0,100] range
    def x2svg(x):
        return 100.0 * (x-xmin)/(xmax-xmin)
    
    def y2svg(y):
        return height * (y-ymin)/(ymax-ymin)
        
    # Convert svg coordinates to nodes positions
    def svg2x(x):
        return xmin + x * (xmax-xmin) / 100.0
    
    def svg2y(y):
        return ymin + y * (ymax-ymin) / height
        
    # ID of the selected node    
    selected_node = -1
    
    def createSVG():        
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 100 %d" xml:space="preserve">' % int(height)

        # CSS styling
        svg += '''
            <style type="text/css">
               @import url('%s');
            </style>
        ''' % (fontsettings.font_url)

        for edge, value in edges.items():
            n1 = edge[0]
            n2 = edge[1]
            if n1 in nodes_pos and n2 in nodes_pos:
                x1 = x2svg(nodes_pos[n1][0])
                y1 = y2svg(nodes_pos[n1][1])
                x2 = x2svg(nodes_pos[n2][0])
                y2 = y2svg(nodes_pos[n2][1])
                tooltip = nodes_label[n1] + '\n' + nodes_label[n2] + '\n%s: %f' % (edge_label,value)
                svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s;stroke-width:%f"><title>%s</title></line>' % (x1,y1, x2,y2, edgestrokecolor,edgestrokewidth, tooltip)


        for node, coords in nodes_pos.items():
            x = x2svg(coords[0])
            y = y2svg(coords[1])
            color = nodes_color[node]
            name  = nodes_name[node]
            label = nodes_label[node]

            sc = nodestrokecolor
            sw = nodestrokewidth
            if node == selected_node:
                sc = selectedcolor
                sw = selectedstrokewidth
                
            svg += '<circle cx="%f" cy="%f" fill="%s" r="%f" style="stroke:%s;stroke-width:%f"><title>%s</title></circle>' % (x,y,color,radiussvg,sc,sw,label)
            svg += '<text style="pointer-events: none" text-anchor="middle" x="%f" y="%f" font-size="%f" fill="%s" font-weight="500">%s</text>' % (x, y+fontsize/3, fontsize, textcolor, name)


        svg += '</svg>'
        return svg
    
    # Create an output widget and display SVG in it
    if isinstance(width, int):
        w = '%dpx' % width
    elif isinstance(width, float):
        w = '%fpx' % width
    else:
        w = str(width)
        
    out = widgets.Output(layout=Layout(width=w, height='calc(calc(%s * %f) + 18px)' % (w,0.01*height)))

    svg = createSVG()
    with out:
        display(HTML(svg))

    d = Event(source=out, watched_events=['click'])

    def handle_event(event):
        nonlocal selected_node
        
        x = event['relativeX']
        y = event['relativeY']
        w = event['boundingRectWidth']
        h = event['boundingRectHeight']
        xsvg = (x / w) * 100.0
        ysvg = (y / h) * height
        
        xnode = svg2x(xsvg)
        ynode = svg2y(ysvg)
        
        r = svg2x(50.0+radiussvg) - svg2x(50.0)
        
        new_selected_node = -1
        for node, coords in nodes_pos.items():
            x = coords[0]
            y = coords[1]
            if math.hypot(xnode - x, ynode - y) <= r:
                if node == selected_node:
                    new_selected_node = -1
                else:
                    new_selected_node = node

        if new_selected_node != selected_node:
            selected_node = new_selected_node
            if not onclick is None:
                onclick(selected_node)
            out.clear_output(wait=True)
            with out:
                display(HTML(createSVG()))
        

    d.on_dom_event(handle_event)
        
    return out
