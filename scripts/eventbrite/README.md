To pull events from LEEDS 2023 Eventbrite
Run `python .\scripts\eventbrite\info_organisation.py 14487847966 "scripts\eventbrite\attrs.txt" "data/metrics/eventbrite/leeds_2023_events.csv" start.utc`

To create geojson file of events
Run `python .\scripts\eventbrite\process_event_data.py`