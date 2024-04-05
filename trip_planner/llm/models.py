from typing import Literal

from pydantic import BaseModel, Field


class Neighborhood(BaseModel):
    name: str
    description: str
    type: Literal["tourist", "local", "party", "family", "other"]
    walking_score: float


class Activity(BaseModel):
    name: str
    time: Literal["morning", "afternoon", "evening", "night"]
    price: Literal["Free", "$", "$$", "$$$", "$$$$"]
    cost_per_person: float
    type: Literal[
        "restaurant",
        "museum",
        "park",
        "beach",
        "shopping",
        "hiking",
        "sightseeing",
        "bar",
        "nightclub",
        "other",
    ]
    description: str
    url: str = ""


class TravelGuide(BaseModel):
    neighborhoods: list[Neighborhood]
    activities: list[Activity]


class Day(BaseModel):
    day_num: int
    timeline: list[Activity]


class Itinerary(BaseModel):
    areas_to_stay: list[Neighborhood]
    days: list[Day]
