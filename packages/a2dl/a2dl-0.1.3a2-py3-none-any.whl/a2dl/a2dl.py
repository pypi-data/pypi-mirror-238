"""
a2dl | (A)sciidoc(2D)rawio(L)ibrary | https://tigabeatz.net | MIT Licence

- Generates draw.io libraries from AsciiDoc-based descriptions.
- Updates icons within draw.io diagrams based on those libraries.

"""

"""
CORE
"""

from a2dl.core.constants import GLOB_STRING as GLOB_STRING
from a2dl.core.constants import LINES2SKIP as LINES2SKIP
from a2dl.core.constants import ADOC_VARIABLE_IDENTIFIER as ADOC_VARIABLE_IDENTIFIER
from a2dl.core.constants import ADOC_ICON_IDENTIFIER as ADOC_ICON_IDENTIFIER
from a2dl.core.constants import ADOC_ICON_TITLE_IDENTIFIER as ADOC_ICON_TITLE_IDENTIFIER
from a2dl.core.constants import ADOC_ICON_MORE_IDENTIFIER as ADOC_ICON_MORE_IDENTIFIER

from a2dl.core.constants import HTML_TOOLTIP as HTML_TOOLTIP
from a2dl.core.constants import HTML_SECTION as HTML_SECTION
from a2dl.core.constants import HTML_WARNING as HTML_WARNING
from a2dl.core.constants import HTML_MORE_BASEURL as HTML_MORE_BASEURL
from a2dl.core.constants import HTML_MORE as HTML_MORE

from a2dl.core.constants import ICON_STYLE as ICON_STYLE
from a2dl.core.constants import IMAGE_STYLE as IMAGE_STYLE
from a2dl.core.constants import ARTICLE_TEMPLATE as ARTICLE_TEMPLATE

from a2dl.core.constants import IMAGES_PATH as IMAGES_PATH
from a2dl.core.constants import IMAGES_GLOB_STRING as IMAGES_GLOB_STRING
from a2dl.core.constants import IMAGES_WIDTH as IMAGES_WIDTH
from a2dl.core.constants import IMAGES_HEIGHT as IMAGES_HEIGHT
from a2dl.core.constants import IMAGES_ENFORCE_SIZE as IMAGES_ENFORCE_SIZE

from a2dl.core.constants import GRAPH_EDGE_STYLE as GRAPH_EDGE_STYLE
from a2dl.core.constants import GRAPH_BOX_STYLE as GRAPH_BOX_STYLE
from a2dl.core.constants import GRAPH_IMAGES_HEIGHT as GRAPH_IMAGES_HEIGHT
from a2dl.core.constants import GRAPH_IMAGES_WIDTH as GRAPH_IMAGES_WIDTH

from a2dl.core.constants import DIAGRAM_SETUP as DIAGRAM_SETUP
from a2dl.core.constants import GRAPH_VALUE_SCALES as GRAPH_VALUE_SCALES

from a2dl.core.constants import logging as logging
from a2dl.core.constants import logger as logger
from a2dl.core.constants import get_package_data_path as get_package_data_path

from a2dl.core.icon import Diagicon as Diagicon
from a2dl.core.library import Diaglibrary as Diaglibrary
from a2dl.core.diagram import Diagdiagram as Diagdiagram

"""
File Format EXTENSIONS
"""
from a2dl.extensions.convert import to_pptx
from a2dl.extensions.convert import to_docx
from a2dl.extensions.convert import to_ea

"""
Helpers EXTENSIONS
"""
from a2dl.extensions.helpers import make_example as make_example

"""
Graph EXTENSIONS
"""
from a2dl.extensions.relation import IconRelation as IconRelation
from a2dl.extensions.relation import IconRelations as IconRelations

"""
AI EXTENSIONS
ai based functions to generate diagrams, images, texts and icons.
"""
# from a2dl.extensions.constants import MODEL_GPU_TEXT as MODEL_GPU_TEXT
# from a2dl.extensions.constants import MODEL_CPU_TEXT as MODEL_CPU_TEXT
#
# from a2dl.extensions.constants import MODEL_GPU_TEXT2IMAGE as MODEL_GPU_TEXT2IMAGE
# from a2dl.extensions.constants import MODEL_CPU_TEXT2IMAGE as MODEL_CPU_TEXT2IMAGE
#
# from a2dl.extensions.ai import feed as feed

"""
CLI
"""
from a2dl.cli import cli as cli

if __name__ == '__main__':
    cli()
