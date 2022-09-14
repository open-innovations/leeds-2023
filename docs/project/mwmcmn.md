---
title: My World, My City, My Neighbourhood
templateEngine: njk,md
summary: |
  TBC
links:
  metrics:
    title: My World, My City, My Neighbourhood
    link: /metrics/mwmcmn/
    summary: The metrics page for My World, My City, My Neighbourhood.
---

  Some summary text will go here soon.


  We will continue to develop on these visualisations over the coming weeks and months.


  This projects page will link to the My World My City My Neighbourhood Metrics page below to view the data. 


  {% comp "grid.autogrid" -%}
  {%- for id, link in links -%}
    {{- comp.grid.link(link) | safe -}}
  {%- endfor -%}
{% endcomp %}

