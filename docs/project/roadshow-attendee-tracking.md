---
title: Roadshow Attendee Tracking
summary: Tracking the audience demographics starts now, with assessment of the attendees at the LEEDS 2023 roadshows.
templateEngine: njk,md
links:
  metrics:
    title: Roadshow Attendees
    link: /metrics/roadshow-attendees/
    summary: The metrics page for the roadshow attendees.
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

{% comp "grid.autogrid" -%}
  {%- for id, link in links -%}
    {{- comp.grid.link(link) | safe -}}
  {%- endfor -%}
{% endcomp %}
