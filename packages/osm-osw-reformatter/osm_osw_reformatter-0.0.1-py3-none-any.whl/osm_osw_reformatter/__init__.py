import os
from pathlib import Path
from .osm2osw.osm2osw import OSM2OSW

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path used for generation the files.
DOWNLOAD_FOLDER = f'{Path.cwd()}/tmp'


class Formatter:
    def __init__(self, workdir=DOWNLOAD_FOLDER, pbf_file=None):
        is_exists = os.path.exists(workdir)
        if not is_exists:
            os.makedirs(workdir)
        self.workdir = workdir
        self.pbf_file = pbf_file

    async def osm2osw(self) -> bool:
        convert = OSM2OSW(pbf_file=self.pbf_file, workdir=self.workdir)
        return await convert.convert()
