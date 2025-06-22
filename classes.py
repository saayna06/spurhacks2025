from __future__ import annotations
from datetime import datetime
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from typing import Any
import re



# ------------------ MISSION CLASS ------------------

class Mission:
    def __init__(
        self,
        seeker: User,
        description: str,
        title: str,
        urgency: str,
        start_datetime: datetime,
        end_datetime: datetime,
        postal_code: str,
        google_api_key: str
    ) -> None:
        self.seeker = seeker
        self.title = title
        self.description = description
        self.urgency = urgency
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.keywords = description.split()
        self.completed = False

        geolocator = GoogleV3(api_key=google_api_key, timeout=10)
        self.location = geolocator.geocode(postal_code)
        if not self.location:
            raise ValueError("Invalid postal code for mission.")
        self.lat = self.location.latitude
        self.long = self.location.longitude
        self.coords = (self.lat, self.long)

        self.requested_users = []

    def complete(self) -> None:
        self.completed = True


# ------------------ USER CLASS ------------------

class User:
    def __init__(
        self,
        name: str,
        postal_code: str,
        user_id: str,
        bio: str,
        age: int,
        email: str,
        phone_num: str,
        google_api_key: str
    ):
        # --- Validation ---
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name must be alphabetic.")
        if not user_id.isalnum() or len(user_id) > 20:
            raise ValueError("Invalid user ID.")

        self.name = name
        self.user_id = user_id
        self.bio = bio
        self.age = age
        self.email = email
        self.phone_num = phone_num
        self.skills = []
        self.reviews = {}
        self.text_log = {}
        self.postal_code = postal_code

        geolocator = GoogleV3(api_key=google_api_key, timeout=10)
        self.location = geolocator.geocode(postal_code)
        if not self.location:
            raise ValueError("Invalid postal code for user.")
        self.lat = self.location.latitude
        self.long = self.location.longitude
        self.coords = (self.lat, self.long)

        # import MissionBoard here just once, then assign homepage
        from missionboard import MissionBoard
        self.homepage = MissionBoard([], self)