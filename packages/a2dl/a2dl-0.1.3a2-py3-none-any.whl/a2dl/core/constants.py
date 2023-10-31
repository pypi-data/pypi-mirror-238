import logging
import importlib.resources

# The following string determines the file search pattern:
GLOB_STRING = '**/*.adoc'  # Search for all adoc files recursively

# Detecting relevant lines in files can be customized with the following strings:
ADOC_VARIABLE_IDENTIFIER = [["==", "===", "====", "====="],
                            ":variable_name:"]  # Extract content afer each identifier until the next occurrence of i in [0]
ADOC_ICON_IDENTIFIER = ":icon_image_rel_path:"
ADOC_ICON_TITLE_IDENTIFIER = ":icon_name:"
ADOC_ICON_MORE_IDENTIFIER = ":read_more:"
LINES2SKIP = ['[quote', 'image::']  # skips lines starting with

# Formatting of the Tooltip can be customized with the following strings:
HTML_TOOLTIP = '<h1 class="dio_tooltip" >%name%</h1>'  # The HTML for each section will get appended to this string
HTML_SECTION = '<h2 class="dio_tooltip" >{}</h2>%{}%'  # variable['title'], variable['name']
HTML_WARNING = '<b class="dio_tooltip" >{}</b>'

# "read more" will be the last line in the html tooltip
HTML_MORE_BASEURL = '{}'  # 'or: use a base ur like https://example.com/{}
#      if articles details page share the same base url'
HTML_MORE = '<br> <a href="{}" target="_more">Image generated with Stable Diffusion</a>'

# Icon styling
ICON_STYLE = "rounded=1;whiteSpace=wrap;html=1;"

# If sections include images as .png, these will be encoded and included. The image styling can be modified:
IMAGE_STYLE = 'fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/{},{};'  # The type and image data are set from the file

# Generator settings
ARTICLE_TEMPLATE = 'data/template_article.adoc'
IMAGES_PATH = 'data/images'
IMAGES_GLOB_STRING = '**/*.png'
IMAGES_WIDTH = "70"
IMAGES_HEIGHT = "70"
IMAGES_ENFORCE_SIZE = True

# Graph
# how shall the arrows look?
GRAPH_EDGE_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;"
# style of a box, if a node is not found in a library
GRAPH_BOX_STYLE = "rounded=1;whiteSpace=wrap;html=1;"
GRAPH_LAYOUT = 'spring'  # spiral, spectral, shell, circular, spring
GRAPH_SCALE = 20
GRAPH_CENTER = (500, 500)
GRAPH_IMAGES_WIDTH: str = "70"
GRAPH_IMAGES_HEIGHT: str = "70"
GRAPH_VALUE_SCALES: tuple[float, float, float, float] = (-1.0, 1.0, 0.0, 3000.0)


# Diagram
DIAGRAM_SETUP: dict = {
    "dx": "1114",
    "dy": "822",
    "pageWidth": "1169",
    "pageHeight": "827"
}

# While updating a diagram, these attributes of used icons in a diagram will not get overwritten
EXCLUDE_ATTRIBS: list[str] = ['x', 'y', 'width', 'height', 'id', 'name']

# create logger
logger = logging.getLogger('a2dl')
logger.setLevel(logging.INFO)
sh = logging.NullHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


def get_package_data_path(filename: str, p: bool = False) -> str:
    if p:
        ref = importlib.resources.files('a2dl.data') / filename
        with importlib.resources.as_file(ref) as path:
            strpath = str(path)
        return strpath
    else:
        return f'data/{filename}'
