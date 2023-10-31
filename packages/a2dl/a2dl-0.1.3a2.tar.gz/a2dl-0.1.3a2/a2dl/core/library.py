import glob
import hashlib
import json
import uuid
import xml.etree.ElementTree as ET
from os.path import abspath, join, basename

from a2dl.core.constants import GLOB_STRING
from a2dl.core.constants import logger, get_package_data_path
from a2dl.core.icon import Diagicon


class Diaglibrary:
    """
    A class to represent a Draw.IO Library which handles collections of `Diagicon` objects.

    Example Usage:

    # by image
    >>> my_icon = Diagicon(name='tigabeatz')
    >>> x = my_icon.from_adoc(get_package_data_path('examples/exampleDocument.adoc'))
    >>> my_library = Diaglibrary()
    >>> my_library.icons.append(my_icon)
    >>> my_library.names.append(my_icon.name)
    >>> my_library.write(get_package_data_path('test/test-generated-library-from-exampleDocument.xml'))

    # from folder
    >>> my_library2 = Diaglibrary()
    >>> my_library2.from_folder(get_package_data_path('.'))
    >>> my_library2.write(get_package_data_path('test/test-generated-library-from-data-folder.xml'))

    """

    def __init__(self, libraryid: str = None, name: str = None):
        """ Initializes a new diaglibrary instance.
        """

        if not libraryid:
            self.libraryid: str = str(uuid.uuid1())
        else:
            self.libraryid: str = libraryid

        self.name: str = name
        self.names: list[str] = []
        self.icons: list[Diagicon] = []  # instances of type icon
        self.w: int = 50
        self.h: int = 50
        self.image_base_path: str = None

    def __backup__(self):
        """ backup the library if overwrite """
        pass

    def __as_object__(self) -> ET.Element:

        mxlibrary = ET.Element("mxlibrary")
        tmpl = []
        for icn in self.icons:
            tmpl.append(
                {
                    "xml": icn.as_object_s(),
                    "w": self.w,
                    "h": self.h
                })

        mxlibrary.text = json.dumps(tmpl, indent=2)
        return mxlibrary

    @staticmethod
    def __read_library2dict__(filename: str) -> list:
        """
        read a draw.io library and return as dict

        >>> hashlib.sha256(json.dumps(Diaglibrary.__read_library2dict__(get_package_data_path('examples/exampleLibrary.xml')), sort_keys=True).encode('utf-8')).hexdigest()
        '6b243484f07fa2e04c382b834e962c58377475f4b005f6ca2836e1bfa05b5af1'
        """

        tree = ET.parse(abspath(filename))
        root = tree.getroot()
        data = json.loads(root.text)
        xmlobjects = []

        for xmldict in data:
            xmlobject = ET.fromstring(xmldict['xml'])
            icon = {"tag": xmlobject[0].tag, "elements": []}
            for el in xmlobject[0]:
                icon['elements'].append({"tag": el.tag, "attrib": el.attrib})
            xmlobjects.append(icon)

        return xmlobjects

    def write(self, file: str):
        """write as a library file"""

        # todo: check if corretly written as utf 8

        try:
            tree = ET.ElementTree(self.__as_object__())
            tree.write(abspath(file), encoding="unicode")
        except TypeError as err:
            logger.critical(f'{file} {err}')

    def from_folder(self, path: str):
        files = glob.glob(join(abspath(path), GLOB_STRING), recursive=True)
        self.name = str(basename(path))
        for file in files:
            try:
                icn = Diagicon()
                icn.image_base_path = self.image_base_path
                icn.from_adoc(file)
                self.names.append(icn.name)
                self.icons.append(icn)
            except ValueError as wrn:
                logger.warning(f'{file}, {wrn}')
            except Exception as err:
                logger.error(f'{file}, {err}')

        logger.debug(f'files: {len(files)} ')
        logger.debug(f'icons: {len(self.icons)} ')

        for logicon in self.icons:
            logger.debug(f'{logicon.variables} {logicon.image}')
