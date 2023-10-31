import glob
import xml.etree.ElementTree as ET
import uuid

from os import makedirs
from os.path import abspath, join, dirname, basename
from shutil import copytree

from a2dl.core.constants import ARTICLE_TEMPLATE, IMAGES_PATH, IMAGES_GLOB_STRING
from a2dl.core.constants import IMAGES_WIDTH, IMAGES_HEIGHT
from a2dl.core.constants import logger, get_package_data_path
from a2dl.core.icon import Diagicon
from a2dl.core.library import Diaglibrary

""" handle template files """


def apply_template(image_name="", image_link="", image_alt_text="", image_h=IMAGES_HEIGHT, image_w=IMAGES_WIDTH,
                   image_rel_path="", image_text=""):
    """
    :icon_image_rel_path: {{image_rel_path}}
    :icon_name: {{image_name}}
    :read_more: {{image_link}}
    [[sec-{{image_name}}]]
    == {{image_name}}
    image::{icon_image_rel_path}[{{image_alt_text}},{{image_w}},{{image_h}},float="right"]
    === {{image_name}} Summary
    """

    searchies = [
        ('{{image_name}}', image_name.strip('\n').strip())
        , ('{{image_link}}', image_link.strip('\n').strip())
        , ('{{image_alt_text}}', image_alt_text.strip('\n').strip())
        , ('{{image_h}}', image_h.strip('\n').strip())
        , ('{{image_w}}', image_w.strip('\n').strip())
        , ('{{image_rel_path}}', image_rel_path.strip('\n').strip())
        , ('{{image_text}}', image_text.strip('\n').strip())
    ]

    try:

        nt = []
        with open(abspath(ARTICLE_TEMPLATE), "r") as file:
            fileslines = file.readlines()
            for line in fileslines:
                for searcher in searchies:
                    if searcher[0] in line:
                        line = line.replace(searcher[0], str(searcher[1]))
                nt.append(line)
        return nt

    except FileNotFoundError as err:
        logger.error(err)
        return None


def make_example(target_path: str = 'test/'):
    """  Generates a folder with articles images library

    >>> make_example()

    """

    # create dir
    makedirs(dirname(abspath(target_path)), exist_ok=True)

    # images
    images = glob.glob(join(abspath(IMAGES_PATH), IMAGES_GLOB_STRING), recursive=True)
    # IMAGES_PATH = get_package_data_path(abspath(target_path))
    try:
        copytree(get_package_data_path('examples/images', p=True), abspath(target_path), dirs_exist_ok=True)
    except FileNotFoundError as err:
        logger.error(err)
        copytree(get_package_data_path('examples/images'), abspath(target_path), dirs_exist_ok=True)

    # generate icons, articles and library
    library = Diaglibrary()
    for imagepath in images:
        icon = Diagicon()

        # article
        article = (
            apply_template(
                image_name=basename(imagepath).strip(".png"),
                image_rel_path=join(abspath(target_path), basename(imagepath)),
                image_link=f"#{basename(imagepath).strip('.png')}",
                image_alt_text=f'image {basename(imagepath)} is a random generated image',
                image_h=IMAGES_WIDTH,
                image_w=IMAGES_HEIGHT
            ),
            basename(imagepath)
        )
        tap = join(abspath(target_path), f'{basename(imagepath).strip(".png")}.adoc')

        targetarticle = open(tap, "w")
        targetarticle.writelines(article[0])
        targetarticle.close()

        # icon
        x = icon.from_adoc(tap)
        icon.image = imagepath
        icon.width = IMAGES_WIDTH
        icon.height = IMAGES_HEIGHT

        library.icons.append(icon)

    # library
    library.w = IMAGES_WIDTH
    library.h = IMAGES_HEIGHT
    library.write(join(target_path, 'test-generated-library.xml'))



""" Elements of a draw.io diagram

    For now, this is not used within the rest of the package.
    I just drop here what i notice during experiments.

"""


class Diagram:
    """ The basic draw.io diagram structure. """

    def __init__(self):
        mxfile = ET.Element("mxfile")
        diagram = ET.SubElement(mxfile, "diagram", name="Page-1", id=str(uuid.uuid1()))
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel",
                                     dx="1114", dy="822", grid="1", gridSize="10",
                                     guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                                     pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")

        root = ET.SubElement(mxGraphModel, "root")
        mxCellDiagId0 = ET.SubElement(root, "mxCell", id="0")
        mxCellDiagId1 = ET.SubElement(root, "mxCell", id="1", parent="0")

        self.data = mxfile

    def get(self) -> ET.Element:
        return self.data


class ImageNode:
    """ The basic draw.io "Icon" structure. """

    def __init__(self,
                 objectid: str, parent: ET.SubElement,
                 style: str, vertex: str,
                 height: str, width: str,
                 x: str, y: str):
        self.objectid = objectid
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style
        self.vertex = vertex

        xmlobject = ET.SubElement(parent, "object")
        xmlobject.set("id", self.objectid)
        xmlobject.set("label", self.objectid)
        xmlobject.set("name", self.objectid)

        mxCell = ET.SubElement(xmlobject, "mxCell")
        mxCell.set("parent", self.parent)
        mxCell.set("vertex", self.vertex)
        mxCell.set("style", self.style)

        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", self.x)
        mxGeometry.set("y", self.y)
        mxGeometry.set("width", self.width)
        mxGeometry.set("height", self.height)
        mxGeometry.set("as", "geometry")

        self.data = xmlobject

    def get(self) -> ET.SubElement:
        return self.data


class Node:
    """ The basic draw.io "Blank Icon" structure. """

    def __init__(self,
                 objectid: str, parent: ET.SubElement,
                 style: str, vertex: str,
                 height: str, width: str,
                 x: str, y: str,
                 value: str):
        self.objectid = objectid
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style
        self.vertex = vertex
        self.value = value

        mxCell = ET.SubElement(parent, "mxCell")
        mxCell.set("id", self.objectid)
        mxCell.set("parent", self.parent)
        mxCell.set("vertex", self.vertex)
        mxCell.set("value", self.value)
        mxCell.set("style", self.style)

        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", self.x)
        mxGeometry.set("y", self.y)
        mxGeometry.set("width", self.width)
        mxGeometry.set("height", self.height)
        mxGeometry.set("as", "geometry")

        self.data = mxCell

    def get(self) -> ET.SubElement:
        return self.data


class Edge:
    """ The basic draw.io "Edge" structure.
    """

    def __init__(self,
                 linkid: str, parent: ET.SubElement,
                 style: str, vertex: str,
                 height: str, width: str,
                 x: str, y: str,
                 value: str, source: str, target: str):
        self.linkid = linkid
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style
        self.vertex = vertex
        self.value = value
        self.source = source
        self.target = target

        mxCell = ET.SubElement(parent, "mxCell")
        mxCell.set("id", self.linkid)
        mxCell.set("parent", self.parent)
        mxCell.set("vertex", self.vertex)

        mxCell.set("source", self.source)
        mxCell.set("target", self.target)
        mxCell.set("value", self.value)

        mxCell.set("style", self.style)
        mxCell.set("edge", "1")

        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("relative", "1")
        mxGeometry.set("as", "geometry")

        self.data = mxCell

    def get(self) -> ET.SubElement:
        return self.data


def style_o_mat(source_style: str, target_style: str, exclude_style: list = None) -> str:
    """  Extracts css styles from strings, and return a string of styles with the styles merged.
        String format: "fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png,iVBORw0KGgoAAAANSUhEUgAAAgAAACC;"
    """

    EXCLUDE_STYLES: list[str] = ['x', 'y', 'width', 'height']

    if exclude_style is None:
        exclude_style = EXCLUDE_STYLES

    def style_extract(style: str):
        styles = style.split(';')  # list of style=value
        styletupels = []
        for stylestr in styles:
            styletupel = stylestr.split('=')  # tuple of (style, value)
        return styletupels

    s_style_list = style_extract(source_style)
    t_style_list = style_extract(target_style)

    print(s_style_list, t_style_list)

    return ' '
