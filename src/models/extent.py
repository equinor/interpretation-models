from pydantic import BaseModel, field_validator


class Point(BaseModel):
    """A 2D coordinate point."""

    x: float
    y: float


class Extent(BaseModel):
    """A polygon extent defined by corner points."""

    points: list[Point]

    @field_validator("points")
    @classmethod
    def validate_minimum_points(cls, v):
        if len(v) < 3:
            raise ValueError("Extent must have at least 3 points to form a polygon")
        return v

    @property
    def is_closed(self) -> bool:
        """Check if the polygon is closed (first and last points are the same)."""
        if len(self.points) < 2:
            return False
        return self.points[0] == self.points[-1]

    def close(self) -> None:
        """Close the polygon by appending the first point at the end if not already closed."""
        if not self.is_closed and len(self.points) > 0:
            self.points.append(self.points[0])
