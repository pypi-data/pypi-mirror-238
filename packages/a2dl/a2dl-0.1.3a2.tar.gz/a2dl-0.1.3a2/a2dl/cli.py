import sys
from os import getcwd

from a2dl.core.constants import logger
from a2dl.core.diagram import Diagdiagram
from a2dl.extensions.helpers import make_example
from a2dl.core.library import Diaglibrary


def cli():
    if not len(sys.argv) == 3:
        logger.critical(
            "The script is called with {} arguments, but needs at least two: "
            "-> 'a2dl --library path/to/folder-to-scan path/to/library-file-to-write.xml' "
            "-> 'a2dl --diagram path/to/folder-to-scan path/to/file-to-update' "
            "-> 'a2dl --example path/to/folder-to-write".format(
                len(sys.argv) - 1))
        sys.exit(1)
    else:

        cwd = getcwd()
        logger.info(f'workdir: {cwd}')

        if sys.argv[1] == '--example' and sys.argv[2]:
            logger.info(f'Creating Example {sys.argv[2]}')
            make_example(sys.argv[2])
            logger.info(f'Done with creating example {sys.argv[2]}')
        elif sys.argv[1] == '--library' and sys.argv[2] and sys.argv[3]:
            logger.info('source: {} '.format(sys.argv[2]))
            logger.info('target: {} '.format(sys.argv[3]))

            logger.info('Creating library')
            my_library2 = Diaglibrary()
            my_library2.from_folder(sys.argv[2])
            my_library2.write(sys.argv[3])
            logger.info('Done with creating library')

        elif sys.argv[1] == '--diagram' and sys.argv[2] and sys.argv[3]:
            logger.info('source: {} '.format(sys.argv[2]))
            logger.info('target: {} '.format(sys.argv[3]))

            DL = Diaglibrary()
            DL.from_folder(sys.argv[2])

            logger.info('Updating Diagram')
            DG = Diagdiagram()
            DG.from_file(sys.argv[3])
            DG.update(libraries=[DL])
            logger.info('Done with updating Diagram')
