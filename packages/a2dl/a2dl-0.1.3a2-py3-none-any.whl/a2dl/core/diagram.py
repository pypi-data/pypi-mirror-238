import base64
import hashlib
import os
import xml.etree.ElementTree as ET
import zlib
from os.path import abspath, join, dirname, basename
from urllib.parse import unquote

from a2dl.core.constants import logger, get_package_data_path, EXCLUDE_ATTRIBS
from a2dl.core.library import Diaglibrary


class Diagdiagram:
    """
    A class to represent a Draw.IO Diagram.

    This class enables the manipulation and updating of Draw.IO Diagrams
    based on provided libraries of icons (Diaglibrary).

    Usage example:

    >>> # create library
    >>> DL = Diaglibrary()
    >>> DL.image_base_path = get_package_data_path('.')
    >>> DL.from_folder(get_package_data_path('.'))
    >>> # read Diagran
    >>> DG = Diagdiagram()
    >>> DG.from_file(get_package_data_path('exampleDiagramFromLibrary-old.drawio'))
    >>> # set options
    >>> DG.clean = False # remove backup files
    >>> DG.backup = 'test-.$exampleDiagramFromLibrary-old.drawio.bkp'
    >>> DG.new_file = True  # set False to overwrite file or True to overwrite {filename}.new.drawio. will not create a backup, if set
    >>> # update Diagram
    >>> DG.update(libraries=[DL])
    >>> # update a compressed Diagram
    >>> DG.from_file(get_package_data_path('exampleDiagramFromLibrary-compressed-old.drawio'))
    >>> DG.update(libraries=[DL])

    """

    def __init__(self):
        """ Initializes a new diagDiagram instance. """
        self.filepath: str = None  # of str
        self.objects: ET.Element = None  # of xml.etree.ElementTree.Element
        self.stamps = []  # of __stamp__
        self.tree: ET.ElementTree = None  # of xml.etree.ElementTree
        self.libraries = []  # of Diaglibrary
        self.backup = None  # set by self.from_file()
        self.clean: bool = False  # remove backup files
        self.was_compressed: bool = False  # if read a compressed file
        self.new_file: bool = True  # set False to overwrite file or True to overwrite {filename}.new.drawio

    def __backup__(self):
        """ backup the original diagram -> rename as .${filename}.bkp """
        if self.backup:
            if not self.new_file:
                os.rename(abspath(self.filepath), self.backup)

    def __restore__(self):
        """ restore the original diagram -> rename as filename """
        if self.backup and os.path.exists(self.backup):
            if not self.new_file:
                os.rename(self.backup, abspath(self.filepath))

    def __clean__(self):
        """ remove backup files"""
        if self.backup and self.clean and os.path.exists(self.backup):
            if not self.new_file:
                os.remove(self.backup)

    def __handle_compressed__(self, data):

        def pako_inflate_raw(data):
            # https://crashlaker.github.io/programming/2020/05/17/draw.io_decompress_xml_python.html
            decompress = zlib.decompressobj(-15)
            decompressed_data = decompress.decompress(data)
            decompressed_data += decompress.flush()
            return decompressed_data

        compdat = data.find('.//diagram').text

        a = base64.b64decode(compdat)
        b = pako_inflate_raw(a)
        c = unquote(b.decode())

        dat = ET.fromstring(c)

        return dat

    def __stamp__(self, xmlobject: ET.Element) -> tuple[str, str, str, str]:
        """
        get an icons name, label, hash of the image, hash of the attributes
        :param xmlobject: xml.etree.ElementTree.Element
        :return: (str, str, str, str)
        """

        mxcell = xmlobject.find('mxCell')

        sattribs = str(xmlobject.items())
        sname = str(xmlobject.get('name'))
        slabel = str(xmlobject.get('label'))

        try:
            simage = str(mxcell.get('style').split('image=data:image/png,')[1].strip(';'))
        except AttributeError as err:
            logger.warning(f'{err}, {self.filepath}')
            raise ValueError('no image')

        return (sname, slabel, hashlib.sha256(simage.encode('utf-8')).hexdigest(), hashlib.sha256(
            sattribs.encode('utf-8')).hexdigest())

    def __read__(self):
        self.tree = ET.parse(abspath(self.filepath))
        root = self.tree.getroot()
        self.objects = root.findall('.//object')

        if not self.objects:
            self.objects = self.__handle_compressed__(root).findall('.//object')
            self.was_compressed = True

        # stamp each icon for a later update
        for xmlobject in self.objects:
            self.stamps.append(self.__stamp__(xmlobject))

    def from_file(self, filepath: str):
        """
        Reads a diagram file and initializes the Diagdiagram object.

        >>> DG = Diagdiagram()
        >>> DG.from_file(get_package_data_path('exampleDiagramFromLibrary-old.drawio'))
        >>> basename(DG.filepath)
        'exampleDiagramFromLibrary-old.drawio'
        """
        self.filepath = filepath
        if not self.backup:
            self.backup = abspath(join(dirname(self.filepath), f'.${basename(self.filepath)}.bkp'))
        # read diagram file
        self.__read__()

    def update(self, libraries: list):
        """
        Updates the diagram based on the provided libraries.

        >>> DL = Diaglibrary()
        >>> DL.image_base_path = get_package_data_path('.')
        >>> DL.from_folder(get_package_data_path('.'))
        >>> DG = Diagdiagram()
        >>> DG.from_file(get_package_data_path('exampleDiagramFromLibrary-old.drawio'))
        >>> DG.update(libraries=[DL])
        >>> len(DG.libraries)
        1
        """

        self.libraries = libraries
        root = self.tree.getroot()

        for icnlib in self.libraries:
            logger.debug(f'Updater working at file {self.filepath} with library {icnlib.name}')
            # update per library and icon
            for icn in icnlib.icons:
                # update the object within the diagram
                try:

                    object_element = root.findall(f".//object[@name='{icn.name}']")
                    for diagram_icon in object_element:

                        # diagram icon
                        diagram_cel = diagram_icon.find("mxCell")

                        # library icon
                        library_icon = icn.__as_object__()  # diagram_cel
                        library_cel = library_icon.find("mxCell")

                        # replace attributes
                        for li in library_icon.attrib:
                            if li not in EXCLUDE_ATTRIBS:  # if not li == 'id' and not li == 'name':
                                logger.debug(f'updating {li} in icon {icn.name} ')
                                diagram_icon.set(li, library_icon.get(li))

                        for di in library_cel.attrib:
                            if not di == 'id' and not di == 'name':
                                logger.debug(f'updating {di} in icon {icn.name} ')
                                diagram_cel.set(di, library_cel.get(di))

                except AttributeError as err:
                    logger.error(f'{err} with file {self.filepath}')

        # write updated file
        self.__backup__()
        try:
            if not self.new_file:
                self.tree.write(abspath(self.filepath))
            else:
                self.tree.write(abspath(self.filepath + '.new.drawio'))
        except Exception as err:
            logger.error(f'{err} with file {self.filepath}')
            self.__restore__()

        # if enabled, remove backup files
        self.__clean__()

        logger.info(f'Updated: {self.filepath}')
