import os
import asyncio
from pathlib import Path
from ..serializer.counters import WayCounter, PointCounter, NodeCounter
from ..helpers.osw import OSWHelper


class OSM2OSW:
    def __init__(self, pbf_file=None, workdir=None):
        self.pbf_path = str(Path(pbf_file))
        self.filename = os.path.basename(pbf_file).replace('.pbf', '').replace('.osm', '')
        self.workdir = workdir

    async def convert(self):
        try:

            print('Estimating number of ways, nodes and points in datasets...')
            tasks = [
                OSWHelper.count_entities(self.pbf_path, WayCounter),
                OSWHelper.count_entities(self.pbf_path, NodeCounter),
                OSWHelper.count_entities(self.pbf_path, PointCounter)
            ]

            count_results = await asyncio.gather(*tasks)

            print('Creating networks from region extracts...')
            tasks = [OSWHelper.get_osm_graph(self.pbf_path)]
            osm_graph_results = await asyncio.gather(*tasks)
            osm_graph_results = list(osm_graph_results)
            for OG in osm_graph_results:
                await OSWHelper.simplify_og(OG)

            for OG in osm_graph_results:
                await OSWHelper.construct_geometries(OG)

            for OG in osm_graph_results:
                await OSWHelper.write_og(self.workdir, self.filename, OG)

            print(f'Created OSW files!')
            return True
        except Exception as error:
            print(error)
            return False
