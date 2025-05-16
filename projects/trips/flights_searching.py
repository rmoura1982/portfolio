from connections import API_KEY
from serpapi import GoogleSearch
import pandas as pd
from datetime import datetime, timedelta


def search_fly(**kwargs):
  if 'returning' in kwargs:
    params = {
      "api_key": API_KEY,
      "engine": "google_flights",
      "hl": "en",
      "gl": "us",
      "departure_id": kwargs.get('departure'),
      "arrival_id": kwargs.get('arrival'),
      "outbound_date": kwargs.get('outbound'),
      "return_date": kwargs.get('returning'),
      "currency": "USD",
      "type": "1"
    }
  else:
    params = {
      "api_key": API_KEY,
      "engine": "google_flights",
      "hl": "en",
      "gl": "us",
      "departure_id": kwargs.get('departure'),
      "arrival_id": kwargs.get('arrival'),
      "outbound_date": kwargs.get('outbound'),
      "currency": "USD",
      "type": "2"
    }

  try:
    search = GoogleSearch(params)
  except Exception as e:
    print(e)

  results = search.get_dict()
  return results


def search_metadata(data):
  metadata = {
    "id": data["search_metadata"].get("id"),
    "created_at": data["search_metadata"].get("created_at"),
    "processed_at": data["search_metadata"].get("processed_at"),
  }

  try:
    df = pd.DataFrame([metadata])
  except Exception as e:
    print(e)

  return df


def flights_data():
  trip_starting = (datetime.now() + timedelta(days=90)).date()
  trip_end = (trip_starting + timedelta(days=20))
  kwargs = {
    "departure": "PHL",
    "arrival": "GRU",
    "outbound": trip_starting.strftime("%Y-%m-%d"),
    "returning": trip_end.strftime("%Y-%m-%d")
  }
  
  results = search_fly(**kwargs)
  return results


def process_flights(data):
  voos = []
  for flight in data.get("best_flights", []):
    df = flight.get("flights", [])
    if not df:
      continue 
    summary = {
      "time_departure_first_flight": df[0]["departure_airport"].get("time"),
      "departure_first_flight": df[0]["departure_airport"].get("name"),
      "id_departure_first_flight": df[0]["departure_airport"].get("id"),
      "airplane_departure_first_flight": df[0].get("airline"),
      "travel_class_departure_first_flight": df[0].get("travel_class"),
      "flight_number_departure_first_flight": df[0].get("flight_number"),
      "duration_departure_first_flight": df[0].get("duration"),
      "time_darrival_first_flight": df[0]["arrival_airport"].get("time"),
      "darrival_first_flight": df[0]["arrival_airport"].get("name"),
      "id_arrival_first_flight": df[0]["arrival_airport"].get("id"),
      "layovers": flight.get("layovers", [{}])[0].get("duration"),
      "price": flight.get("price"),
    }

    if len(df) > 1:
      summary.update(
        {
          "time_departure_second_flight": df[1]["departure_airport"].get("time"),
          "departure_second_flight": df[1]["departure_airport"].get("name"),
          "id_departure_second_flight": df[1]["departure_airport"].get("id"),
          "airplane_departure_second_flight": df[1].get("airline"),
          "travel_class_departure_second_flight": df[1].get("travel_class"),
          "flight_number_departure_second_flight": df[1].get("flight_number"),
          "duration_departure_second_flight": df[1].get("duration"),
          "time_darrival_second_flight": df[1]["arrival_airport"].get("time"),
          "darrival_second_flight": df[1]["arrival_airport"].get("name"),
          "id_arrival_second_flight": df[1]["arrival_airport"].get("id"),
        }
      )

    try:
      voos.append(summary)
    except Exception as e:
      print(e)
      
  return pd.DataFrame(voos)


def data_merge():
  df_search_metadata = search_metadata(flights_data())
  df_process_flights = process_flights(flights_data())

  metadata_values = df_search_metadata.iloc[0].to_dict()
  df = df_process_flights.assign(**metadata_values)

  return df
