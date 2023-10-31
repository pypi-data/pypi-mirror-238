import base64
import hashlib
import json
import logging
import re
import struct
import uuid
import xml.etree.ElementTree as ET
from os.path import abspath, join, dirname

from a2dl.core.constants import ADOC_ICON_TITLE_IDENTIFIER, ADOC_ICON_MORE_IDENTIFIER
from a2dl.core.constants import ADOC_VARIABLE_IDENTIFIER, ADOC_ICON_IDENTIFIER, IMAGES_WIDTH, IMAGES_HEIGHT, \
    IMAGES_ENFORCE_SIZE
from a2dl.core.constants import HTML_TOOLTIP, HTML_SECTION, HTML_WARNING, HTML_MORE_BASEURL, HTML_MORE
from a2dl.core.constants import ICON_STYLE, IMAGE_STYLE
from a2dl.core.constants import LINES2SKIP
from a2dl.core.constants import logger, get_package_data_path


class Diagicon:
    """
    A class to represent a Draw.IO Icon, allowing conversion from AsciiDoc files to Draw.IO diagram files.

    Example Usage:

    >>> my_icon = Diagicon()
    >>> x = my_icon.from_adoc(get_package_data_path('exampleDocument.adoc'))
    >>> # write the icon to a Diagram file
    >>> my_icon.write_diagram(get_package_data_path('test-generated-icon-from-exampleDocument.drawio'))

    """

    def __init__(self, iconid: str = None, name: str = None):
        """ Initializes a new diagicon instance.

        :param iconid: The unique ID for the icon. If none is provided, a UUID is generated.
        :param name:  The name for the icon. If none is provided, the id is used.
        """
        self.tooltip: str = 'HTML_TOOLTIP'
        self.html_section: str = HTML_SECTION

        if not iconid:
            self.iconid = str(uuid.uuid1())
        else:
            self.iconid = iconid
        if not name:
            self.name = self.iconid
        else:
            self.name = name

        self.placeholders: str = "1"
        self.link: str = None
        self.image: str = None
        self.variables: list = None  # [{"title":label, "name":label, "content":[] }]
        self.parent: str = "1"
        self.vertex: str = "1"
        self.x: str = "0"  # NEED 4 DIAGRAM
        self.y: str = "0"  # NEED 4 DIAGRAM
        self.width: str = IMAGES_WIDTH
        self.height: str = IMAGES_HEIGHT
        self.style = ICON_STYLE
        self.image_base_path: str = None
        self.enforcesize: bool = IMAGES_ENFORCE_SIZE

    @staticmethod
    def __read_diagram2dict__(filename: str) -> list:
        """
        read a draw.io diagram and return as dict

        >>> retval = Diagicon.__read_diagram2dict__(get_package_data_path('exampleDiagram.drawio'))
        >>> hashlib.sha256(json.dumps(retval, sort_keys=True).encode('utf-8')).hexdigest()
        '3689e6d92d8cce691334888734486e683c865af6f6e5ff1111474aca920c7e0f'
        """

        tree = ET.parse(filename)
        root = tree.getroot()

        # data = base64.b64decode(root.text)
        # xml = zlib.decompress(data, wbits=-15)
        # xml = unquote(xml.decode('utf-8'))

        xmlobjects = []

        for xmldict in root:
            for xmlobject in xmldict[0][0]:
                if xmlobject.tag == 'object':
                    icon = {"tag": xmlobject.tag, "attrib": xmlobject.attrib, "elements": []}
                    for el in xmlobject:
                        icon['elements'].append({"tag": el.tag, "attrib": el.attrib, "elements": []})
                        for shape in el:
                            icon['elements'].append({"tag": shape.tag, "attrib": shape.attrib})
                    xmlobjects.append(icon)

        return xmlobjects

    @staticmethod
    def __get_base64_encoded_image__(image_path: str):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except FileNotFoundError as err:
            logger.error(err)

    @staticmethod
    def __get_image_size__(file_path: str):
        try:
            with open(file_path, 'rb') as f:
                data = f.read(24)
            if len(data) != 24:
                logger.warning(f'The file {file_path} is not a PNG image.')
                return None, None
            if data[:8] != b'\x89PNG\r\n\x1a\n':
                logger.warning(f'The file {file_path} is not a PNG image.')
                return None, None

            width, height = struct.unpack('>LL', data[16:24])
            logger.debug(f'The file {file_path} is a PNG image with width: {width} and height: {height}.')

            return width, height
        except FileNotFoundError as err:
            logging.error(str(err))

    def __as_object__(self, parent: ET.Element = None) -> ET.Element:
        if parent:
            xmlobject = ET.SubElement(parent, "object")
        else:
            xmlobject = ET.Element("object")

        xmlobject.set("id", self.iconid)
        xmlobject.set("label", self.name)  # SPECIAL used when icon is used library
        xmlobject.set("name", self.name)
        xmlobject.set("placeholders", self.placeholders)

        # any custom fields
        for variable in self.variables:
            vt = ''
            for l in variable['content']:
                vt = vt + str(l)
            xmlobject.set(variable['name'], vt)
            self.tooltip = HTML_TOOLTIP + self.html_section.format(variable['title'], variable['name'])

        # add readmore
        if self.link:
            xmlobject.set("link", HTML_MORE_BASEURL.format(self.link))
            self.tooltip = self.tooltip + HTML_MORE.format(HTML_MORE_BASEURL.format(self.link))

        xmlobject.set("tooltip", self.tooltip)

        mxCell = ET.SubElement(xmlobject, "mxCell")
        mxCell.set("parent", self.parent)
        mxCell.set("vertex", self.vertex)

        # image
        if self.image:
            if self.image.endswith('.png'):
                if not self.enforcesize:
                    self.width, self.height = self.__get_image_size__(self.image)
                else:
                    self.width, self.height = IMAGES_WIDTH, IMAGES_HEIGHT
                if self.width:
                    mxCell.set("style", IMAGE_STYLE.format('png', self.__get_base64_encoded_image__(self.image)))
            else:
                logger.warning('fileformat for {} not implemented: {}'.format(self.name, self.image))

        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", str(self.x))
        mxGeometry.set("y", str(self.y))
        mxGeometry.set("width", str(self.width))
        mxGeometry.set("height", str(self.height))
        mxGeometry.set("as", "geometry")

        return xmlobject

    def __as_diagram__(self) -> ET.Element:
        # The element tree
        mxfile = ET.Element("mxfile")
        diagram = ET.SubElement(mxfile, "diagram",
                                name="Page-1", id=str(uuid.uuid1()))
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel",
                                     dx="1114", dy="822", grid="1", gridSize="10",
                                     guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                                     pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        mxCelldiag1 = ET.SubElement(root, "mxCell",
                                    id="0")
        mxCelldiag2 = ET.SubElement(root, "mxCell",
                                    id="1", parent="0")
        xmlobject = self.__as_object__(root)
        return mxfile

    def as_object(self, parent: ET.Element = None) -> ET.Element:
        """to embed in other xml structures"""
        return self.__as_object__(parent)

    def as_object_s(self) -> str:
        """to embed in other library xml structures"""
        mxGraphModel = ET.Element("mxGraphModel")
        root = ET.SubElement(mxGraphModel, "root")
        mxCelldiag1 = ET.SubElement(root, "mxCell",
                                    id="0")
        mxCelldiag2 = ET.SubElement(root, "mxCell",
                                    id="1", parent="0")
        asd = self.__as_object__(parent=root)
        rt = None
        try:
            rt = ET.tostring(mxGraphModel).decode(encoding='utf-8')
        except Exception as err:
            logger.error(f'{self.name} {self.iconid} {err}')
        return rt

    def as_diagram_s(self) -> str:
        """return a string of diagram xlm"""
        xmlstr = ET.tostring(self.__as_diagram__())
        return xmlstr

    def write_diagram(self, file: str):
        """write as a diagram file"""
        try:
            tree = ET.ElementTree(self.__as_diagram__())
            tree.write(abspath(file))
        except TypeError as err:
            logger.error(f'Can not write file: {err} Does the source file exist? Is it in good shape?')

    @staticmethod
    def linerules(oline: str) -> str:
        """add special line handling, like make asciidoc url to html url"""
        # exchange link
        if "http" in oline:
            # get url, domain, link description "(^http.?://(.*))\[(.*)\]"
            words = oline.split()
            uline = oline
            for word in words:
                m = re.search("(^http.?://(.*))\[(.*)\]", word)
                # todo: change regex, such that any text inside the [] works (breaks with whitespace, actually)
                if m:
                    # logger.debug(m.group(3))
                    if len(m.group(3)) < 3:
                        mn = '<a href="{}" target="_blank">{}<a>'.format(m.group(1), m.group(2))
                    else:
                        mn = '<a href="{}" target="_blank">{}<a>'.format(m.group(1), m.group(3))
                    uline = oline.replace(m.group(0), mn)
                    # logger.debug(uline)
            logger.debug(f'replacing {oline} with {uline}')
            return uline

        # replace Warning
        elif oline.startswith('WARNING:'):
            uline = HTML_WARNING.format(oline.strip("WARNING:").strip())
            logger.debug(f'replacing {oline} with {uline}')
            return uline

        else:

            # strip adoc image lines, quotes and such
            for stripsign in LINES2SKIP:
                if oline.startswith(stripsign):
                    uline = ''
                    logger.debug(f'replacing {oline} with {uline}')
                    return uline

            return oline

    def from_adoc(self, filename: str, parent: ET.Element = None):
        """set from adoc and return as object"""

        def get_data(lines):
            variables = []
            icon_full_path = None
            starts = []

            def extract(s, e):
                c = []
                i = 0
                for eline in lines:
                    if s + 3 <= i <= e:
                        # c.append(line)
                        found = False
                        for l2_ident in ADOC_VARIABLE_IDENTIFIER[0]:
                            if eline.startswith(l2_ident):
                                found = True
                        if not found:
                            # special line handling, like make url tags ...
                            nline = self.linerules(eline)
                            c.append(nline)
                        else:
                            break
                    i += 1
                return c

            # start
            line_number = 0
            for line in lines:
                # --> the variables are repeated
                for l1_ident in ADOC_VARIABLE_IDENTIFIER[0]:
                    if line.startswith(l1_ident) and lines[line_number + 1].startswith(ADOC_VARIABLE_IDENTIFIER[1]):
                        variables.append({
                            "title": line.strip(l1_ident).strip(),
                            "name": lines[line_number + 1].strip(ADOC_VARIABLE_IDENTIFIER[1]).strip(),
                            "start": line_number,
                        })
                        starts.append(line_number)
                        break

                if line.startswith(ADOC_ICON_IDENTIFIER):
                    if not self.image_base_path:
                        icon_full_path = abspath(join(dirname(filename), line.strip(ADOC_ICON_IDENTIFIER).strip()))
                    else:
                        icon_full_path = abspath(join(self.image_base_path, line.strip(ADOC_ICON_IDENTIFIER).strip()))
                    self.icon = icon_full_path

                if line.startswith(ADOC_ICON_TITLE_IDENTIFIER):
                    self.name = line.strip(ADOC_ICON_TITLE_IDENTIFIER).strip()
                    self.iconid = self.name

                if line.startswith(ADOC_ICON_MORE_IDENTIFIER):
                    self.link = line.strip(ADOC_ICON_MORE_IDENTIFIER).strip()

                line_number += 1

            # end
            for variable in variables:
                cnt = 0
                for start in starts:
                    if variable['start'] == start:
                        try:
                            variable['end'] = starts[cnt + 1] - 1
                        except Exception as err:
                            variable['end'] = len(lines)
                            logging.debug(err)
                    cnt += 1

            # content
            for variable in variables:
                variable['content'] = extract(variable['start'], variable['end'])

            return variables, icon_full_path

        # todo: check if files are read correctly as UTF 8

        try:
            with open(filename, "r") as file:
                fileslines = file.readlines()

            self.variables, self.image = get_data(fileslines)
            logger.debug(f'{filename} {len(self.variables)} {self.image}')

            if len(self.variables) == 0 and not self.image:
                raise ValueError('is not an icon file and will be sKipped')
            else:
                return self.__as_object__(parent)

        except FileNotFoundError as err:
            logger.error(err)

        return None
