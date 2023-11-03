import logging
import sys
from pathlib import Path

from omf.fileio import OMFWriter
from omf.fileio.geoh5 import GeoH5Reader

_logger = logging.getLogger(__package__)


def run():
    geoh5_filepath = Path(sys.argv[1])
    if len(sys.argv) < 3:
        output_filepath = geoh5_filepath.with_suffix(".omf")
    else:
        output_filepath = Path(sys.argv[2])
        if not output_filepath.suffix:
            output_filepath = output_filepath.with_suffix(".omf")
    if output_filepath.exists():
        _logger.error(
            "Cowardly refuses to overwrite existing file '%s'.", output_filepath
        )
        sys.exit(1)

    reader = GeoH5Reader(geoh5_filepath)
    OMFWriter(reader(), str(output_filepath.absolute()))
    _logger.info("OMF file created: %s", output_filepath)


if __name__ == "__main__":
    run()
