from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from trip_planner.llm.models import TravelGuide

set_llm_cache(InMemoryCache())


class TravelAgent:
    def __init__(self):
        self.model = ChatOpenAI(temperature=0.5, max_tokens=5000)

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
                    This is a {trip_type}. {additional_info}\n{format_instructions}
                    """,
                ),
            ],
        )

        self.parser = PydanticOutputParser(pydantic_object=TravelGuide)

    async def get_recs(
        self,
        destination: str,
        num_days: int,
        num_people: int,
        trip_type: str,
        additional_info: str = "",
    ) -> TravelGuide:
        chain = self.prompt | self.model | self.parser
        response = chain.ainvoke(
            {
                "destination": destination,
                "num_days": num_days,
                "num_people": num_people,
                "trip_type": trip_type,
                "additional_info": additional_info,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        return await response
