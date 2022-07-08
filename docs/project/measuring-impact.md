---
title: Measuring the Impact of Leeds2023
templateEngine: njk,md
summary: |
  We're building interactive, data-driven dashboards that show the impact of LEEDS 2023.

links:
  needs:
    title: Leeds2023 Data Needs
    link: https://docs.google.com/spreadsheets/d/1w0d8F6biPXG8cawiOr8akKDlrx9_eUZfLSQCcPLwtrg/edit#gid=0
    summary: A working document summarising the data needs for Leeds2023.
---

The team are taking a careful approach to ensuring that the impact of the LEEDS 2023 events is tracked and reported.
We are working with our evaluation partners to build the data framework which will collate, process and present the
impact. This will include baseline information about the socio-economic, cutural and tourism background to the region, as well as
specifically collected surveys which measure outputs.

As a starting point, we will pull together some of the economic targets drawn from baseline research and
analysis by BOP Consulting, using a variety of open data sources. We will then build on these to feed into
a framework for evaluating the reach, impact and performance of Leeds2023 and in the years ahead.

It is early days for this work, but we aim to start publishing these figures here in the coming months. 

{% comp "grid.autogrid" -%}
  {%- for id, link in links -%}
    {{- comp.grid.link(link) | safe -}}
  {%- endfor -%}
{% endcomp %}

## Wireframe

The key visualisations from economic baseline research will be transferred onto the Leeds 2023 Impact Dashboard in future, however for now we will be pulling together the visualisations roughly outlined below. The wireframe below was created on [this Miro board](https://miro.com/app/board/uXjVOWlUNu8=/?share_link_id=501874732910). 

![Wireframe of the structure of the Economic Baseline Report](/assets/images/Economic%20Baseline%20Report.png "Wireframe for the Economic Baseline Report")
