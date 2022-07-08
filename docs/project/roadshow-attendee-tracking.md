---
title: Roadshow Attendee Tracking
summary: Tracking the audience demographics starts now, with assessment of the attendees at the LEEDS 2023 roadshows.
templateEngine: njk,md
---

The team are running a series of events such as roadshows promoting the year of culture. We will publish and visualise the
events, and look to ways to undertake demographic analysis.

The minimum set of data per event is:
 
* Name of event
* Details of programme of work / series
* Location of event (address with postcode, to enable plotting on a map)
* Number of attendees
* Name of person hosting the event / entering the data

This is currently collected via Typeform, which has an [API to collect responses][TYPEFORM_RESPONSES].

If possible, we'd like to collect a set of postcodes for as many attendees as possible, which will enable 
analysis of engagement across Leeds wards per event, and also help with segmentation using the Open Audience tool.
 
We would not rely on this data in place of an separate independent count of number of attendees. Having these two measures would give a view of how many of the attendees gave information about their residence (for tests of statistical significance)

[TYPEFORM_RESPONSES]: https://developer.typeform.com/responses/

## Sample visualisations

This [Hex cartogram](https://open-innovations.org/blog/2017-05-08-mapping-election-with-hexes) shows number of roadshow attendees who
submitted Typeform responses categorised by their ward of residence (based on their supplied postcode).

{% include "visualisations/roadshow-attendees/ward-hex.njk" %}

{% include "visualisations/roadshow-attendees/cumulative-graph.njk" %}

This shows the cumulative feedback submitted.
