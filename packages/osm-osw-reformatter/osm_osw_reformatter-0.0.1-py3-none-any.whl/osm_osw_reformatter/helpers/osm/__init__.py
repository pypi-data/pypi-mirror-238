import asyncio
from ...serializer.osw.osw_normalizer import OSWWayNormalizer, OSWNodeNormalizer, OSWPointNormalizer
from ...serializer.osm.osm_graph import OSMGraph


async def count_entities(pbf_path: str, counter_class):
    loop = asyncio.get_event_loop()
    counter = counter_class()
    await loop.run_in_executor(None, counter.apply_file, pbf_path)
    return counter.count


async def get_osm_graph(pbf_path):
    loop = asyncio.get_event_loop()
    OG = await loop.run_in_executor(
        None,
        OSMGraph.from_pbf,
        pbf_path,
        osw_way_filter,
        osw_node_filter,
        osw_point_filter
    )

    return OG


def osw_way_filter(tags):
    normalizer = OSWWayNormalizer(tags)
    return normalizer.filter()


def osw_node_filter(tags):
    normalizer = OSWNodeNormalizer(tags)
    return normalizer.filter()


def osw_point_filter(tags):
    normalizer = OSWPointNormalizer(tags)
    return normalizer.filter()


async def simplify_og(og):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, og.simplify)


async def construct_geometries(og):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, og.construct_geometries)
