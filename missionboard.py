from __future__ import annotations
from datetime import date
from geopy.distance import geodesic
from typing import Optional
from classes import Mission
from classes import User 

mission_database = []

class MissionBoard:
    def __init__(self, missions: list[Mission], curr_user: Optional[User] = None) -> None:
        self.missions = missions
        self.curr_user = curr_user
        self.radius = 10

    def find_in_radius(self, radius_km: float) -> MissionBoard:
        if not self.curr_user:
            # If no current user, return all missions as is
            return self
        user_coords = (self.curr_user.lat, self.curr_user.long)
        filtered = [
            mission for mission in self.missions
            if geodesic(mission.coords, user_coords).km <= radius_km
        ]
        return MissionBoard(filtered, self.curr_user)