""" View and generate projects """
import uuid
import xml.etree.ElementTree as ET
from os.path import abspath

import matplotlib.pyplot as plt
import networkx as nx

from a2dl.core.constants import logger, GRAPH_EDGE_STYLE, GRAPH_BOX_STYLE, GRAPH_IMAGES_HEIGHT, GRAPH_IMAGES_WIDTH
from a2dl.core.constants import GRAPH_SCALE, GRAPH_CENTER, GRAPH_LAYOUT, DIAGRAM_SETUP, GRAPH_VALUE_SCALES, \
    get_package_data_path
from a2dl.core.library import Diaglibrary

""" Relationships
    generate and return draw.io diagram as object with the library icons and their relationships
"""


class IconRelation:
    def __init__(self):
        """
        source : str name of the icon linking to me
        target: str name of the icon i am linking to
        unidir: bool set True (no direction arrow) or False (with direction arrow from source -> target)
        properties: list of strings which will be applied to the links text
        """
        self.source: str = None
        self.target: str = None
        self.unidir: bool = True
        self.properties: list[str] = []
        self.nodes: list[dict] = []
        self.link: dict = None
        self.__nxgraph__: nx.Graph = None

    def __prepare_as_graph__(self):
        G = nx.Graph()

        linkid = f'{self.source}-{self.target}'

        snode = {
            'id': self.source,
            'name': self.source,
            'label': self.source,
        }
        self.nodes.append({'data': snode, 'classes': 'a2dl_node'})
        G.add_node(self.source, name=self.source, label=self.source)

        tnode = {
            'id': self.target,
            'name': self.target,
            'label': self.target,
        }
        self.nodes.append({'data': tnode, 'classes': 'a2dl_node'})
        G.add_node(self.source, name=self.source, label=self.source)

        link = {
            'id': linkid,
            'label': str(self.properties).replace('[', ' ').replace(']', ' '),
            'source': self.source,
            'target': self.target,
            'weight': 1
        }
        self.link = {'data': link, 'classes': 'a2dl_link'}
        G.add_edge(self.source, self.target, label=link['label'])

        self.__nxgraph__ = G

    def set(self, source: str, target: str, unidir: bool, properties: list[str]):
        self.source = source
        self.target = target
        self.unidir = unidir
        self.properties = properties

        self.__prepare_as_graph__()

    def get(self) -> dict:
        return {

            "source": self.source,
            "target": self.target,
            "unidir": self.unidir,
            "properties": self.properties
        }


class IconRelations:
    """

    >>> DL = Diaglibrary()
    >>> DL.from_folder(get_package_data_path('.'))
    >>> # create a graph network diagram of library icons
    >>> # list of tuples with each:
    >>> #      0 - Source Icon Name,
    >>> #      1 - Target Icon Name,
    >>> #      2 - True/False for arrow on a connection,
    >>> #      3 - List of Labels to show on the connection
    >>> IRL = [
    >>>     ('IconOverview', 'Example', False, ['implements']),
    >>>     ('IconOverview', 'UnknownIcon', False, ['uses']),
    >>>     ('byCode', 'IconOverview', True, ['know each other']),
    >>>     ('UnknownIcon', 'byCode', False, ['depends']),
    >>> ]
    >>> IR = IconRelations()
    >>> IR.set(IRL, libraries=[DL])
    >>> IR.write_diagram(get_package_data_path('test/test-generated-diagram-from-graph-data.drawio'))
    """

    def __init__(self):
        self.relations: list[IconRelation] = []
        self.cleaned: tuple[list, list] = None
        self.libraries: list[Diaglibrary] = []

    @staticmethod
    def __new_range__(OldValue: float, OldMin: float = GRAPH_VALUE_SCALES[0],
                      OldMax: float = GRAPH_VALUE_SCALES[1], NewMin: float = GRAPH_VALUE_SCALES[2],
                      NewMax: float = GRAPH_VALUE_SCALES[3]):
        # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
        OldRange = OldMax - OldMin
        if (OldRange == 0):
            NewValue = NewMin
        else:
            NewRange = NewMax - NewMin
            NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        return NewValue

    def __dedup__(self):
        nodesnames, linksnames = [], []
        cnodes, clinks = [], []
        for rel in self.relations:
            # nodes
            for reln in rel.nodes:
                if not reln['data']['name'] in nodesnames:
                    nodesnames.append(reln['data']['name'])
                    cnodes.append(reln)
            # links
            if not rel.link['data']['id'] in linksnames:
                linksnames.append(rel.link['data']['id'])
                clinks.append(rel.link)
        cnodes.extend(clinks)
        self.cleaned = (cnodes, clinks)
        return cnodes

    def __build_nx_graph__(self, layout: str = GRAPH_LAYOUT, tst: bool = False):
        # https://networkx.org/documentation/stable/reference/drawing.html
        H = nx.Graph()
        for rel in self.relations:
            H = nx.compose(rel.__nxgraph__, H)

        # A dictionary of positions keyed by node
        match layout:
            case 'spring':
                pos = nx.spring_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)
            case 'circular':
                pos = nx.circular_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)
            case 'shell':
                pos = nx.shell_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)
            case 'spectral':
                pos = nx.spectral_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)
            case 'spiral':
                pos = nx.spiral_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)
            case _:
                pos = nx.spring_layout(H, scale=GRAPH_SCALE, center=GRAPH_CENTER)

        pos_scale = nx.rescale_layout_dict(pos)
        if tst:
            nx.draw(H, pos=pos_scale, with_labels=True, font_weight='bold')
            plt.show()
        return pos_scale

    def __as_diagram__(self) -> ET.Element:
        # The element tree
        mxfile = ET.Element("mxfile")

        diagram = ET.SubElement(mxfile, "diagram",
                                name="Page-1", id=str(uuid.uuid1()))

        mxGraphModel = ET.SubElement(diagram, "mxGraphModel",
                                     dx=DIAGRAM_SETUP['dx'], dy=DIAGRAM_SETUP['dy'], grid="1", gridSize="10",
                                     guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                                     pageScale="1", pageWidth=DIAGRAM_SETUP['pageWidth'],
                                     pageHeight=DIAGRAM_SETUP['pageHeight'], math="0", shadow="0")

        root = ET.SubElement(mxGraphModel, "root")

        mxCellDiagId0 = ET.SubElement(root, "mxCell", id="0")
        mxCellDiagId1 = ET.SubElement(root, "mxCell", id="1", parent="0")

        # Add nodes with their positions
        gelems = self.__build_nx_graph__(tst=False)
        for icon in gelems:

            logger.debug(f'preparing {icon} ')

            old_x = gelems[icon][0]
            old_y = gelems[icon][1]

            new_x = self.__new_range__(old_x)
            new_y = self.__new_range__(old_y)

            dif_old = new_x / old_x
            dif_new = new_y / old_y

            logger.debug(f'Old position (x, y, delta): {old_x}, {old_y}, {dif_old}')
            logger.debug(f'New position (x, y, delta): {new_x}, {new_y}, {dif_new}')

            # if the icon we are working at is not in a libray, the use a default icon style.
            # otherwise, use the library icon
            not_found = True
            for lib in self.libraries:
                logger.info(f'{str(lib.names)} are the Icons in Library {lib.name}')
                if str(icon) in lib.names:
                    logger.debug(f'{str(icon)} found in Library')
                    not_found = False
                    for icn in lib.icons:
                        if str(icn.name) == str(icon):
                            icn.x = new_x
                            icn.y = new_y
                            icn.width = GRAPH_IMAGES_WIDTH
                            icn.height = GRAPH_IMAGES_HEIGHT
                            xmlobject = icn.__as_object__(parent=root)

            if not_found:
                logger.debug(f'{str(icon)} NOT found in Library')
                mxCell = ET.SubElement(root, "mxCell", parent="0")
                mxCell.set("id", str(icon))
                mxCell.set("parent", "1")
                mxCell.set("value", str(icon))
                mxCell.set("vertex", "1")
                mxCell.set("style", GRAPH_BOX_STYLE)
                mxGeometry = ET.SubElement(mxCell, "mxGeometry")
                mxGeometry.set("x", str(new_x))
                mxGeometry.set("y", str(new_y))
                mxGeometry.set("width", GRAPH_IMAGES_WIDTH)
                mxGeometry.set("height", GRAPH_IMAGES_HEIGHT)
                mxGeometry.set("as", "geometry")

        # Add edges
        n = self.__dedup__()
        for rel in self.cleaned[1]:
            mxCell = ET.SubElement(root, "mxCell", parent="0")
            mxCell.set("id", str(rel['data']['id']))
            mxCell.set("source", str(rel['data']['source']))
            mxCell.set("target", str(rel['data']['target']))
            mxCell.set("value", str(rel['data']['label']))
            mxCell.set("parent", "1")
            mxCell.set("edge", "1")
            mxCell.set("vertex", "1")
            mxCell.set("style",
                       GRAPH_EDGE_STYLE)
            mxGeometry = ET.SubElement(mxCell, "mxGeometry")
            mxGeometry.set("relative", "1")
            mxGeometry.set("as", "geometry")

        return mxfile

    def __graph__(self):
        self.__as_diagram__()

    def write_diagram(self, file: str):
        """write as a diagram file"""
        tree = ET.ElementTree(self.__as_diagram__())
        tree.write(abspath(file))

    def set(self, rels: list, libraries: list[Diaglibrary] = None):
        for ir in rels:
            rr = IconRelation()
            rr.set(ir[0], ir[1], ir[2], ir[3])
            self.relations.append(rr)
        if libraries:
            self.libraries = libraries
