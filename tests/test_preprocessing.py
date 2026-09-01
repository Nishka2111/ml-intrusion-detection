import numpy as np
from backend.services.features import DATASET_FEATURES, normalise_feature_key
from backend.services.preprocessing import (
    EXPECTED_FEATURE_COUNT,
    align_to_canonical_vector,
    build_model_input,
)


def test_canonical_feature_count():
    assert len(DATASET_FEATURES) == EXPECTED_FEATURE_COUNT == 78


def test_normalise_feature_key():
    assert normalise_feature_key("Destination Port") == "destination_port"
    assert normalise_feature_key("Flow Bytes/s") == "flow_bytes_s"


def test_align_to_canonical_vector_shape():
    row = align_to_canonical_vector({})
    assert row.shape == (1, 78)


def test_align_matches_spaced_and_snake_keys():
    row = align_to_canonical_vector({"Destination Port": 25})
    col = DATASET_FEATURES.index("Destination Port")
    assert row[0, col] == 25.0
