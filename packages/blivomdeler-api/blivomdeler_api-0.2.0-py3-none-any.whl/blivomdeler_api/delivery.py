from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Delivery:
    verified: bool
    start_date: date
    end_date: date
    bundles: int
    bundle_points: int
    distributed_routes: int
    distribution_points: int
    experience_weeks: int
    experience_points: int
    extra_points: int = 0

    @property
    def total_points(self) -> int:
        return (
            self.bundle_points
            + self.distribution_points
            + self.experience_points
            + self.extra_points
        )
