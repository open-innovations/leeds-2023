---
title: Roadshow Attendees
summary: Data about the attendees at the LEEDS 2023 community roadshow events.
metas:
  title: LEEDS 2023 Metrics - Roadshow Attendees
  description: |
    Visualisations of key metrics related to the LEEDS 2023 community roadshow events.
templateEngine: njk,md
---

# {{ title }}

This [Hex cartogram](https://open-innovations.org/blog/2017-05-08-mapping-election-with-hexes) shows number of [Roadshow](https://leeds2023.co.uk/get-ready-for-the-roadshow-with-leeds-2023/) attendees who submitted Typeform responses categorised by their ward of residence (based on their supplied postcode). Both the Hex cartagram and the below chart are updated automatically on a nightly basis. 

Roadshow events are taking place across every ward in Leeds. The below data should not be considered at accurate representation of the number of attendees at any given event, as people will travel across ward boundaries to attend these activities as well as coming from beyond the city of Leeds. 

As the data is drawn automatically from submitted survey responses, it is also not an accurate count of the number of attendees. We will look to visualise this data as it is made available. 


{% include "visualisations/roadshow-attendees/ward-hex.njk" %}


This chart shows the number of Roadshow surveys submitted per week. The value is the cumulative feedback submitted.

{% include "visualisations/roadshow-attendees/cumulative-graph.njk" %}

