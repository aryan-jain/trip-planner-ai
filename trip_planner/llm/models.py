from typing import Literal

from pydantic import BaseModel, Field


class Neighborhood(BaseModel):
    name: str
    description: str
    type: Literal["tourist", "local", "party", "family"]
    walking_score: float


class Restaurant(BaseModel):
    name: str
    price: Literal["$", "$$", "$$$", "$$$$"]
    cuisine: str
    description: str
    url: str


class Activity(BaseModel):
    name: str
    price: Literal["$", "$$", "$$$", "$$$$"]
    description: str
    type: Literal["outdoor", "indoor", "cultural", "party", "sightseeing"]


class BarClub(BaseModel):
    name: str
    price: Literal["$", "$$", "$$$", "$$$$"]
    description: str
    url: str


class TravelGuide(BaseModel):
    neighborhoods: list[Neighborhood]
    restaurants: list[Restaurant]
    activities: list[Activity]
    bars_and_clubs: list[BarClub]


class TimelineItem(BaseModel):
    time: Literal["morning", "afternoon", "evening", "night"]
    activity: Activity | Restaurant | BarClub


class Day(BaseModel):
    day_num: int
    timeline: list[TimelineItem]


class Itinerary(BaseModel):
    days: list[Day]
    cost_low: float
    cost_high: float
