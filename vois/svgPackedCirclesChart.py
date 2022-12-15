"""SVG Packed Circles chart from a pandas DataFrame."""
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
import pandas as pd

import collections
import itertools
import logging
import math
import sys

import plotly.express as px

try:
    from . import colors
    from .vuetify import settings, fontsettings
except:
    import colors
    from vuetify import settings, fontsettings


# Basic circle packing algorithm based on 2 algorithms.
# Circles are first arranged via a version of A1.0 by Huang et al (see
# https://home.mis.u-picardie.fr/~cli/Publis/circle.pdf for details) and then
# enclosed in a circle created around them using Matoušek-Sharir-Welzl algorithm
# used in d3js (see https://beta.observablehq.com/@mbostock/miniball,
# http://www.inf.ethz.ch/personal/emo/PublFiles/SubexLinProg_ALG16_96.pdf, and
# https://github.com/d3/d3-hierarchy/blob/master/src/pack/enclose.js)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
log.addHandler(logging.StreamHandler(sys.stdout))

_eps = sys.float_info.epsilon

_Circle = collections.namedtuple("_Circle", ["x", "y", "r"])
Fields = collections.namedtuple("Fields", ["id", "datum", "children"])


class Circle:
    __slots__ = ["circle", "level", "ex"]

    def __init__(self, x=0.0, y=0.0, r=1.0, level=1, ex=None):
        self.circle = _Circle(x, y, r)
        self.level = level
        self.ex = ex

    def __lt__(self, other):
        return (self.level, self.r) < (other.level, other.r)

    def __eq__(self, other):
        return (self.level, self.circle, self.ex) == (
            other.level,
            other.circle,
            other.ex,
        )

    def __repr__(self):
        return "{}(x={}, y={}, r={}, level={}, ex={!r})".format(
            self.__class__.__name__, self.x, self.y, self.r, self.level, self.ex
        )

    def __iter__(self):
        return [self.x, self.y, self.r].__iter__()

    @property
    def x(self):
        return self.circle.x

    @property
    def y(self):
        return self.circle.y

    @property
    def r(self):
        return self.circle.r


def distance(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    x = x2 - x1
    y = y2 - y1
    return math.sqrt(x * x + y * y) - r1 - r2


def get_intersection(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    dx, dy = x2 - x1, y2 - y1
    d = math.sqrt(dx * dx + dy * dy)
    # Protect this part of the algo with try/except because edge cases
    # can lead to divizion by 0 or sqrt of negative numbers. Those indicate
    # that no intersection can be found and the debug log will show more info.
    try:
        a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
        h = math.sqrt(r1 * r1 - a * a)
    except (ValueError, ZeroDivisionError):
        eps = 1e-9
        if d > r1 + r2:
            log.debug("no solution, the circles are separate: %s, %s", circle1, circle2)
        if d < abs(r1 - r2) + eps:
            log.debug(
                "no solution, circles contained within each other: %s, %s",
                circle1,
                circle2,
            )
        if math.isclose(d, 0, abs_tol=eps) and math.isclose(
            r1, r2, rel_tol=0.0, abs_tol=eps
        ):
            log.debug("no solution, circles are coincident: %s, %s", circle1, circle2)
        return None, None
    xm = x1 + a * dx / d
    ym = y1 + a * dy / d
    xs1 = xm + h * dy / d
    xs2 = xm - h * dy / d
    ys1 = ym - h * dx / d
    ys2 = ym + h * dx / d
    if xs1 == xs2 and ys1 == ys2:
        return (xs1, ys1), None
    return (xs1, ys1), (xs2, ys2)


def get_placement_candidates(radius, c1, c2, margin):
    margin = radius * _eps * 10.0
    ic1 = _Circle(c1.x, c1.y, c1.r + (radius + margin))
    ic2 = _Circle(c2.x, c2.y, c2.r + (radius + margin))
    i1, i2 = get_intersection(ic1, ic2)
    if i1 is None:
        return None, None
    i1_x, i1_y = i1
    candidate1 = _Circle(i1_x, i1_y, radius)
    if i2 is None:
        return candidate1, None
    i2_x, i2_y = i2
    candidate2 = _Circle(i2_x, i2_y, radius)
    return candidate1, candidate2


def get_hole_degree_radius_w(candidate, circles):
    return sum(distance(candidate, c) * c.r for c in circles)


def get_hole_degree_a1_0(candidate, circles):
    return min(distance(candidate, c) for c in circles)


def get_hole_degree_density(candidate, circles):
    return 1.0 - density(circles + [candidate])


def place_new_A1_0(radius, next_, const_placed_circles, get_hole_degree):
    placed_circles = const_placed_circles[:]
    n_circles = len(placed_circles)
    # If there are 2 or less, place circles on each side of (0, 0)
    if n_circles <= 1:
        x = radius if n_circles == 0 else -radius
        circle = _Circle(x, float(0.0), radius)
        placed_circles.append(circle)
        return placed_circles
    mhd = None
    lead_candidate = None
    for (c1, c2) in itertools.combinations(placed_circles, 2):
        margin = radius * _eps * 10.0
        # Placed circles other than the 2 circles used to find the
        # candidate placement.
        other_circles = [c for c in placed_circles if c not in (c1, c2)]
        for cand in get_placement_candidates(radius, c1, c2, margin):
            if cand is None:
                continue
            if not other_circles:
                lead_candidate = cand
                break
            # If overlaps with any, skip this candidate.
            if any(distance(c, cand) < 0.0 for c in other_circles):
                continue
            hd = get_hole_degree(cand, other_circles)
            assert hd is not None, "hole degree should not be None!"
            # If we were to use next_ we could use it here for look ahead.
            if mhd is None or hd < mhd:
                mhd = hd
                lead_candidate = cand
            if abs(mhd) < margin:
                break
    if lead_candidate is None:
        # The radius is set to sqrt(value) in pack_A1_0
        raise ValueError("cannot place circle for value " + str(radius**2))
    placed_circles.append(lead_candidate)
    return placed_circles


def pack_A1_0(data):
    min_max_ratio = min(data) / max(data)
    if min_max_ratio < _eps:
        log.warning(
            "min to max ratio is too low at %f and it could cause algorithm stability issues. Try to remove insignificant data",
            min_max_ratio,
        )
    assert data == sorted(data, reverse=True), "data must be sorted (desc)"
    placed_circles = []
    radiuses = [math.sqrt(value) for value in data]
    for radius, next_ in look_ahead(radiuses):
        placed_circles = place_new_A1_0(
            radius, next_, placed_circles, get_hole_degree_radius_w
        )
    return placed_circles


def extendBasis(B, p):
    if enclosesWeakAll(p, B):
        return [p]

    # If we get here then B must have at least one element.
    for bel in B:
        if enclosesNot(p, bel) and enclosesWeakAll(encloseBasis2(bel, p), B):
            return [bel, p]

    # If we get here then B must have at least two elements.
    for i in range(len(B) - 1):
        for j in range(i + 1, len(B)):
            if (
                enclosesNot(encloseBasis2(B[i], B[j]), p)
                and enclosesNot(encloseBasis2(B[i], p), B[j])
                and enclosesNot(encloseBasis2(B[j], p), B[i])
                and enclosesWeakAll(encloseBasis3(B[i], B[j], p), B)
            ):
                return [B[i], B[j], p]
    raise ValueError("If we get here then something is very wrong")


def enclosesNot(a, b):
    dr = a.r - b.r
    dx = b.x - a.x
    dy = b.y - a.y
    return dr < 0 or dr * dr < dx * dx + dy * dy


def enclosesWeak(a, b):
    dr = a.r - b.r + 1e-6
    dx = b.x - a.x
    dy = b.y - a.y
    return dr > 0 and dr * dr > dx * dx + dy * dy


def enclosesWeakAll(a, B):
    for bel in B:
        if not enclosesWeak(a, bel):
            return False
    return True


def encloseBasis(B):
    if len(B) == 1:
        return B[0]
    elif len(B) == 2:
        return encloseBasis2(B[0], B[1])
    else:
        return encloseBasis3(B[0], B[1], B[2])


def encloseBasis2(a, b):
    x1, y1, r1 = a.x, a.y, a.r
    x2, y2, r2 = b.x, b.y, b.r
    x21 = x2 - x1
    y21 = y2 - y1
    r21 = r2 - r1
    l21 = math.sqrt(x21 * x21 + y21 * y21)
    return _Circle(
        (x1 + x2 + x21 / l21 * r21) / 2,
        (y1 + y2 + y21 / l21 * r21) / 2,
        (l21 + r1 + r2) / 2,
    )


def encloseBasis3(a, b, c):
    x1, y1, r1 = a.x, a.y, a.r
    x2, y2, r2 = b.x, b.y, b.r
    x3, y3, r3 = c.x, c.y, c.r
    a2 = x1 - x2
    a3 = x1 - x3
    b2 = y1 - y2
    b3 = y1 - y3
    c2 = r2 - r1
    c3 = r3 - r1
    d1 = x1 * x1 + y1 * y1 - r1 * r1
    d2 = d1 - x2 * x2 - y2 * y2 + r2 * r2
    d3 = d1 - x3 * x3 - y3 * y3 + r3 * r3
    ab = a3 * b2 - a2 * b3
    xa = (b2 * d3 - b3 * d2) / (ab * 2) - x1
    xb = (b3 * c2 - b2 * c3) / ab
    ya = (a3 * d2 - a2 * d3) / (ab * 2) - y1
    yb = (a2 * c3 - a3 * c2) / ab
    A = xb * xb + yb * yb - 1
    B = 2 * (r1 + xa * xb + ya * yb)
    C = xa * xa + ya * ya - r1 * r1
    if A != 0.0:
        r = -(B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
    else:
        r = -C / B
    return _Circle(x1 + xa + xb * r, y1 + ya + yb * r, r)


def enclose(circles):
    B = []
    p, e = None, None
    # random.shuffle(circles)

    n = len(circles)
    i = 0
    while i < n:
        p = circles[i]
        if e is not None and enclosesWeak(e, p):
            i = i + 1
        else:
            B = extendBasis(B, p)
            e = encloseBasis(B)
            i = 0
    return e


def scale(circle, target, enclosure):
    r = target.r / enclosure.r
    t_x, t_y = target.x, target.y
    e_x, e_y = enclosure.x, enclosure.y
    c_x, c_y, c_r = circle
    return _Circle((c_x - e_x) * r + t_x, (c_y - e_y) * r + t_y, c_r * r)


def density(circles, enclosure=None):
    if not enclosure:
        enclosure = enclose(circles)
    return sum(c.r**2.0 for c in circles if c != enclosure) / enclosure.r**2.0


def look_ahead(iterable, n_elems=1):
    items, nexts = itertools.tee(iterable, 2)
    nexts = itertools.islice(nexts, n_elems, None)
    return itertools.zip_longest(items, nexts)


def _handle(data, level, fields=None):
    if fields is None:
        fields = Fields(None, None, None)
    datum_field = fields.datum if fields.datum else "datum"
    elements = []
    for datum in data:
        if isinstance(datum, dict):
            value = datum[datum_field]
            elements.append(Circle(r=value + 0, level=level, ex=datum))
            continue
        if datum <= 0.0:
            raise ValueError("input data must be positive. Found " + str(datum))
        if datum <= _eps:
            log.warning(
                "input data %f is small and could cause stability issues. Can you scale the data set up or drop insignificant elements?",
                datum,
            )
        try:
            elements.append(Circle(r=datum + 0, level=level, ex={"datum": datum}))
        except TypeError:  # if it fails, assume dict.
            raise TypeError("dict or numeric value expected")
    return sorted(elements, reverse=True)


def _circlify_level(data, target_enclosure, fields, level=1):
    all_circles = []
    if not data:
        return all_circles
    circles = _handle(data, 1, fields)
    packed = pack_A1_0([circle.r for circle in circles])
    enclosure = enclose(packed)
    assert enclosure is not None
    for circle, inner_circle in zip(circles, packed):
        circle.level = level
        circle.circle = scale(inner_circle, target_enclosure, enclosure)
        if circle.ex and fields.children in circle.ex:
            all_circles += _circlify_level(
                circle.ex[fields.children], circle.circle, fields, level + 1
            )
        elif __debug__:
            for key in circle.ex:
                if key not in [fields.id, fields.datum, fields.children]:
                    log.warning("unexpected key '%s' in input is ignored", key)
        all_circles.append(circle)
    return all_circles


def circlify(
    data,
    target_enclosure=None,
    show_enclosure=False,
    datum_field="datum",
    id_field="id",
    children_field="children",
):
    fields = Fields(id=id_field, datum=datum_field, children=children_field)
    if target_enclosure is None:
        target_enclosure = Circle(level=0, x=0.0, y=0.0, r=1.0)
    all_circles = _circlify_level(data, target_enclosure, fields)
    if show_enclosure:
        all_circles.append(target_enclosure)
    return sorted(all_circles)


###########################################################################################################################################################################
# Packed Circles Chart
###########################################################################################################################################################################
def svgPackedCirclesChart(df, valuecolumn, labelcolumn, dimension=30.0,
                          colorlist=px.colors.sequential.Blues,
                          title='', titlecolor='black', titleweight=600, titlecentered=False, titlesize=1.6,
                          labelcolor='black', fontsize=1.3, drawscale=True, scaledigits=2):

    """ Creation of a packed circles chart given an input DataFrame. Labels are taken from the labelcolumn column of the DataFrame, and numerical values from the valuecolumn column. The chart displays the values with proportional size circles packed toward the centre of the chart.
    
    Parameters
    ----------
    df : pandas DataFrame
        Input DataFrame
    valuecolumn : str
        Name of the DataFrame column containing the values to be used for the size of the circles
    labelcolumn : str
        Name of the DataFrame column containing the description of each circle
    dimension : float, optional
        Side of the square containing the chart in vw coordinates (default is 20.0). If drawscale is True, the total height of the chart will be titleh+dimension+fontsize+0.5 vw, otherwise it will be 
    colorlist : list of colors, optional
        List of colors to use for the circles, given their size (default is px.colors.sequential.Blues)
    title : str, optional
        Title of the chart (default is '')
    titlecolor : str, optional
        Color to use for the title (default is 'black')
    titleweight : int, optional
        Font weight to use for the title (default is 600)
    titlecentered : bool, optional
        If True the title will be displayed in center-top position (default is False)
    titlesize : float, optional
        Font size in vw coordinate to use for the title of the chart (default is 1.3)
    labelcolor: str, optional
        Color to use for the labels of the circles (default is 'black')
    fontsize : float, optional
        Font size in vw coordinates to use for the labels of the circles (default is 1.0)
    drawscale : bool, optional
        If Trues, the chart will display an horizontal scale below the circles (default is True)
    scaledigits : int, optional
        Number of decimal digits to display in the tooltip of the scalebar (default is 2)
            
    Returns
    -------
        a string containing SVG code that can be displayed using display(HTML(...))


    Example
    -------
        Creation of a SVG packed circles chart chart to display some values relater to years::

            from IPython.display import display
            import pandas as pd
            import plotly.express as px
            from vois import svgPackedCirclesChart

            table = [['Year', 'Occurrencies'], 
                     [2016, 251],
                     [2017, 239],
                     [2018, 186],
                     [2019, 142],
                     [2020, 59],
                     [2021, 47],
                     [2022, 95],
            ]

            headers = table.pop(0)
            df = pd.DataFrame(table, columns=headers)

            svg = svgPackedCirclesChart.svgPackedCirclesChart(df,
                                                              'Occurrencies',
                                                              'Year',
                                                              dimension=310,
                                                              colorlist=px.colors.sequential.YlOrRd,
                                                              labelcolor='#aaaaaa',
                                                              fontsize=13,
                                                              title='Occurrencies per year:')
            display(HTML(svg))

    .. figure:: figures/packedcircles.png
       :scale: 100 %
       :alt: svgPackedCirclesChart example

       Example of a packed circles chart in SVG
    """

    if df.shape[0] < 1:
        return ''
    
    titleh = 0.0
    if len(title) > 0: titleh = titlesize + 0.4
    
    scaleheight = 0
    displace = -1.0
    if drawscale:
        scaleheight = fontsize
        displace = 0.4
        
    svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0vw" y="0vw" width="%fvw" height="%fvw" xml:space="preserve">' % (dimension,titleh+dimension+scaleheight+displace)

    values = list(df[valuecolumn])
    labels = list(df[labelcolumn])
    
    minvalue = min(values)
    maxvalue = max(values)
    ci = colors.colorInterpolator(colorlist, minValue=minvalue, maxValue=maxvalue)

    circles = circlify(values, show_enclosure=False)
    
    svg += '''
    <style type="text/css">
       @import url('%s');
       .fullrow:hover { stroke: #000044; stroke-width: 2.5px; stroke-dasharray: 2.5,2.5; cursor: pointer; !important; }
    </style>
    ''' % (fontsettings.font_url)

    side = dimension*0.5
    pos = len(circles)-1
    for c in circles:
        tooltip = "%s: %s\n%s: %d" % (labelcolumn, labels[pos], valuecolumn, c.ex['datum'])
        if df.shape[0] == 1: color = colorlist[-1]
        else:                color = ci.GetColor(c.ex['datum'])
        svg += '<circle class="fullrow" cx="%fvw" cy="%fvw" r="%fvw" fill="%s"><title>%s</title></circle>' % (side+c.x*side,titleh+side+c.y*side, c.r*side, color, tooltip)
        if c.r >= 0.1:
            svg += '<text style="pointer-events: none" dominant-baseline="middle" text-anchor="middle" x="%fvw" y="%fvw" font-size="%fvw" fill="%s" style="font-family:%s;" font-weight="600">%s</text>' % (side+c.x*side, titleh+side+c.y*side, fontsize, labelcolor, fontsettings.font_name, labels[pos])
        pos -= 1

    if drawscale:
        ci = colors.colorInterpolator(colorlist,0,1024)
        f = "{:.%df}" % scaledigits
        for i in range(1024):
            x = i*dimension/1024.0
            val = minvalue + i*(maxvalue-minvalue)/1024.0
            sval = f.format(val)
            svg += '<line class="fullrow" x1="%fvw" y1="%fvw" x2="%fvw" y2="%fvw" stroke="%s" stroke-width="2px"><title>%s</title></line>' % (x,titleh+dimension,x,titleh+dimension+2*scaleheight,ci.GetColor(i),sval)
            
        svg += '<text style="pointer-events: none" dominant-baseline="middle" text-anchor="start" x="0.02vw"  y="%fvw" font-size="%fvw" fill="%s" style="font-family:%s;" font-weight="600">%s</text>' % (titleh+dimension+scaleheight/2+0.3, fontsize, labelcolor, fontsettings.font_name, str(min(values)))
        svg += '<text style="pointer-events: none" dominant-baseline="middle" text-anchor="end"   x="%fvw" y="%fvw" font-size="%fvw" fill="%s" style="font-family:%s;" font-weight="600">%s</text>' % (dimension-0.2, titleh+dimension+scaleheight/2+0.3, fontsize, labelcolor, fontsettings.font_name, str(max(values)))

    # Title
    if titlecentered:
        svg += '<text style="pointer-events: none" dominant-baseline="middle" text-anchor="middle" x="%fvw" y="%fvw" font-size="%fvw" fill="%s" style="font-family:%s;" font-weight="600">%s</text>' % (dimension/2.0, titlesize/2.0+0.2, titlesize, 
                                                                                                                                                                                                       titlecolor, fontsettings.font_name, title)
    else:
        svg += '<text style="pointer-events: none" dominant-baseline="middle" text-anchor="start" x="%fvw" y="%fvw" font-size="%fvw" fill="%s" style="font-family:%s;" font-weight="600">%s</text>' % (0.1, titlesize/2.0+0.2, titlesize, 
                                                                                                                                                                                                       titlecolor, fontsettings.font_name, title)
    
    svg += '</svg>'
    return svg
