from datetime import datetime, timezone

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "bulk_utils", str(Path(__file__).resolve().parents[2] / "graphiti_core/utils/bulk_utils.py")
)
bulk_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bulk_utils)
RawEpisode = bulk_utils.RawEpisode

spec_node = importlib.util.spec_from_file_location(
    "nodes", str(Path(__file__).resolve().parents[2] / "graphiti_core/nodes.py")
)
nodes = importlib.util.module_from_spec(spec_node)
spec_node.loader.exec_module(nodes)
EpisodicNode = nodes.EpisodicNode
EpisodeType = nodes.EpisodeType


def test_raw_episode_metadata_preserved():
    meta = {"foo": "bar"}
    raw = RawEpisode(
        name="ep1",
        content="content",
        source_description="src",
        source=EpisodeType.text,
        reference_time=datetime.now(timezone.utc),
        metadata=meta,
    )
    assert raw.metadata == meta

    node = EpisodicNode(
        name=raw.name,
        group_id="g",
        labels=[],
        source=raw.source,
        content=raw.content,
        source_description=raw.source_description,
        created_at=raw.reference_time,
        valid_at=raw.reference_time,
        metadata=raw.metadata,
    )
    assert node.metadata == meta
