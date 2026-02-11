import pytest
from pydantic import ValidationError
from models.extent import Extent, Point


def test_extent_validate_minimum_points_valid():
    """Test that Extent accepts 3 or more points."""
    # Test with exactly 3 points (minimum valid)
    extent = Extent(points=[Point(x=0, y=0), Point(x=1, y=0), Point(x=0, y=1)])
    assert len(extent.points) == 3

    # Test with 4 points
    extent = Extent(
        points=[Point(x=0, y=0), Point(x=1, y=0), Point(x=1, y=1), Point(x=0, y=1)]
    )
    assert len(extent.points) == 4


def test_extent_validate_minimum_points_invalid():
    """Test that Extent rejects less than 3 points."""
    # Test with 2 points (invalid)
    with pytest.raises(ValidationError) as exc_info:
        Extent(points=[Point(x=0, y=0), Point(x=1, y=0)])
    assert "at least 3 points" in str(exc_info.value)

    # Test with 1 point (invalid)
    with pytest.raises(ValidationError) as exc_info:
        Extent(points=[Point(x=0, y=0)])
    assert "at least 3 points" in str(exc_info.value)

    # Test with 0 points (invalid)
    with pytest.raises(ValidationError) as exc_info:
        Extent(points=[])
    assert "at least 3 points" in str(exc_info.value)
