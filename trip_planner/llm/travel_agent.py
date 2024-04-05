import os

from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from trip_planner.llm.models import Itinerary

set_llm_cache(InMemoryCache())


class NotAuthorizedError(Exception): ...


class TravelAgent:
    def __init__(
        self,
        openai_api_key: SecretStr | None = None,
        model_name: str = "gpt-3.5-turbo-1106",
        temperature: float = 0.5,
        max_tokens: int = 4096,
    ):
        if openai_api_key is not None:
            self.model = ChatOpenAI(
                api_key=openai_api_key,
                model="gpt-3.5-turbo-1106",
                temperature=0.5,
                max_tokens=4096,
            )
        elif "OPENAI_API_KEY" in os.environ:
            self.model = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise NotAuthorizedError(
                "OpenAI API key is required. You can either set it in the environment variable OPENAI_API_KEY or set it manually in the settings."
            )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful travel agent AI. You help people plan their trips. 
                    You will help by providing recommendations for areas to stay, things to do, and places to eat.
                    You will also help with budget planning for the trip. Keep your descriptions short.
                    Your responses should be in JSON format.
                    I will provide you with a JSON structure with each request for you to fill in.""",
                ),
                (
                    "human",
                    """
                    Help me plan a trip to {destination}. I want to stay for {num_days} days. We are a group of {num_people} people.
                    This is a {trip_type}. {additional_info}
                    Give me at least 3 options for areas to stay.
                    Make sure to provide a URL for any activities that have a website.
                    For each activity estimate a cost per person in US Dollars and put it in the cost_per_person field.\n
                    {rec_format_instructions} 
                    Make sure your response is valid JSON! 
                    """,
                ),
            ],
        )

        self.parser = PydanticOutputParser(pydantic_object=Itinerary)

    def get_recs(
        self,
        destination: str,
        num_days: int,
        num_people: int,
        trip_type: str,
        additional_info: str = "",
    ) -> Itinerary:
        chain = self.prompt | self.model | self.parser
        response = chain.invoke(
            {
                "destination": destination,
                "num_days": num_days,
                "num_people": num_people,
                "trip_type": trip_type,
                "additional_info": additional_info,
                "rec_format_instructions": self.parser.get_format_instructions(),
            }
        )
        return response
