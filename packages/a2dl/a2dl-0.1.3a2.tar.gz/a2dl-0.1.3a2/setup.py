from setuptools import setup, find_packages

long_description = """

## a2dl | (A)sciidoc(2D)rawio(L)ibrary

This script generates a draw.io library from AsciiDoc-based descriptions and updates diagrams that use icons from these libraries.

- It recursively searches for adoc files in a specified folder and scans for particular lines within these files.
- These lines are then integrated into HTML tooltips of draw.io icons.
- The icons are bundled into a draw.io / diagrams.net library.

I needed to visualize the relationship within previously written content.
I wrote this script to extract relevant information from these articles into tooltips for draw.io icons.
This allows me to concentrate on connecting the information and provide contextual information during a presentation.

### Install

    python3 -m pip install a2dl

### Prepare Asciidoc files

To use this script, simply add the identifiers to any adoc file.

Set these variables at the top of the file

* :icon_image_rel_path: images/generated/3.png
   -> Path to an Icon Image PNG
   
* :icon_name: Icon3
   -> Name for the Icon
   
* :read_more: #sec-icon3
  -> Link for more info, to be appended to the tooltips end

These two lines form the start of a Tooltips content, 
while the first line will also work as a stop sign for the content extraction:

* == or === up to =====

* :variable_name: short_description
  -> choose any name for your variable, but do not include whitespace

### Example Adoc

    :toc:
    :icon_image_rel_path: images/generated/3.png
    :icon_name: Icon3
    :read_more: #sec-icon3
    
    [[sec-icon3]]
    == Icon 3
    
    image::{icon_image_rel_path}[The Icon 3s Alternative Text,160,160,float="right"]
    
    === Short Description
    :variable_name: short_description
    
    This is short Text to Describe the icon
    A short abstract of the Topic
    
    WARNING: Not Safe For Work
    
    
    === XML Attribute 1
    :variable_name: xml_attribute_1
    
    Some part of the text to add to the icons data 

### Use

#### Use in CLI

    python3 -m a2dl --library path/to/folder-to-scan path/to/library-file-to-write.xml
    # OR
    python3 -m a2dl --diagram path/to/folder-to-scan path/to/file-to-update
    # OR
    python3 -m a2dl --example path/to/folder-to-write

or

    a2dl --library path/to/folder-to-scan path/to/library-file-to-write.xml
    # OR
    a2dl --diagram path/to/folder-to-scan path/to/file-to-update
    # OR
    a2dl --example path/to/folder-to-write

#### Use in python script

A basic example. 

    import a2dl.a2dl
    
    # Overwrite some constants
    a2dl.a2dl.ICON_STYLE = "rounded=1;whiteSpace=wrap;html=1;"
    a2dl.a2dl.IMAGE_STYLE = 'fillColor=none;rounded=1;shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/{},{};'
    
    a2dl.a2dl.logging.getLogger('a2dl').addHandler(a2dl.a2dl.logging.NullHandler())
    
    # create icon
    DI = a2dl.a2dl.Diagicon()
    DI.from_adoc('./data/exampleDocument.adoc')
    # write the icon to a Diagram file
    DI.write_diagram('./data/test-generated-icon-from-exampleDocument.drawio')
    
    # create a library
    DL = a2dl.a2dl.Diaglibrary()
    DL.from_folder('./data')
    DL.write('./data/test-generated-library.xml')
    
    #  update a diagram
    DG = a2dl.a2dl.Diagdiagram()
    DG.from_file('./data/exampleDiagramFromLibrary-old.drawio')
    DG.update(libraries=[DL])

"""

setup(
    name='a2dl',
    version='0.1.3a2',
    # packages=['a2dl'],
    packages=find_packages(),
    zip_safe=False,
    package_data={'a2dl': ['data/**/*']},
    install_requires=['python-pptx', 'Pillow', 'python-docx', 'networkx', 'matplotlib'],
    url='https://git.cccwi.de/tigabeatz/a2dl',
    author='tigabeatz',
    author_email='tigabeatz@cccwi.de',
    description='Generate draw.io icon libraries from AsciiDoc-based descriptions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        # "Development Status :: 5 - Production/Stable",
        "Development Status :: 3 - Alpha"
    ],
    entry_points={
        'console_scripts': [
            'a2dl=a2dl.a2dl:cli'
        ]
    },
)
