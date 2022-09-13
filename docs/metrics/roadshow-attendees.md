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

This [Hex cartogram](https://open-innovations.org/blog/2017-05-08-mapping-election-with-hexes) shows the number of people who both attended one of the [Leeds 2023 Roadshow events](https://leeds2023.co.uk/news/get-ready-for-the-roadshow-with-leeds-2023) and submitted Typeform survey responses afterwards. Attendees have been categorised by their ward of residence based on the postcode supplied when they completed the form.  

When viewing the below data, consideration should be given to the fact that residents will travel across ward boundaries to attend events. In addition to this, based on supplied postcodes, others attended Roadshow events from beyond the city of Leeds.

We will visualise a more accurate count of attendees at each Roadshow event as this data is made available.

{%- macro popup(params) -%}
{{ params.label }}</br>
{{ params.value }} attendee returns
{%- endmacro -%}

{% comp 'layout.block', { max_width: '35rem' } %}
{{ comp.charts.hexmap({
  hexjson: hex.wards_leeds,
  data: metrics.roadshow_attendees.by_ward.rows,
  matchKey: 'ward_code',
  valueProp: 'attendees',
  popup: popup
}) | safe }}
{% endcomp %}

Updated automatically on a nightly basis, this chart shows the cumultative number of Roadshow surveys submitted per week.

{% include "visualisations/roadshow-attendees/cumulative-graph.njk" %}

