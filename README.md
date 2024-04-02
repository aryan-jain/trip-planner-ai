# Trip Planner AI
This is your personal AI-assisted travel planner, that uses `gpt-3.5-turbo` to assist with travel planning. It will generate a list of neighborhoods to consider for you to stay in for your trip, along with a day-wise travel itinerary, including restaurants, shopping, sightseeing, museums, bars, nightclubs and any other kind of activity you want to include in your trip. 

### Installation 
#### Installing the dependencies with poetry
```bash
$ git clone git@github.com/aryan-jain/trip-planner-ai
$ cd trip-planner-ai
$ poetry install
```

#### OpenAI API Key
You will need an OpenAI API Key to run the LLM in this app. You can generate one for yourself from [here](https://platform.openai.com/).
Create a `.env` file in the project directory and add the following line to it:
```
OPENAI_API_KEY="<your OpenAI API Key>"
```

### Running the app
```bash
$ streamlit run trip_planner/app.py
```
This will by default run the app on [http://localhost:8501](http://localhost:8501).

### Usage
Fill in the details of your trip in the form, following this guide:

| Field           | Description                                                 | Example                                                                                                                                                                                                                   |
|-----------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Destination     | The destination of the trip.                                | 'San Diego, CA'                                                                                                                                                                                                           |
| Num Days        | The number of days to plan in the itinerary                 | 3                                                                                                                                                                                                                         |
| Num People      | The number of people traveling on this trip, including you. | 4                                                                                                                                                                                                                         |
| Trip Type       | The type of trip this is. "This trip is a _____."           | 'vacation with friends', 'romantic getaway'                                                                                                                                                                               |
| Additional Info | Anything specific you want to include in the itinerary.     | 'We want to experience at least a couple boujee restaurants, but otherwise on a budget. We want to spend one afternoon on the beach. Make sure we get to see at least a few good bars and nightclubs while we are there.' |


Hit `Submit` and the app should generate an itinerary for you.