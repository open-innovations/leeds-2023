---
title: Key Performance Indicator tracker
templateEngine: njk,md
summary: We are automating the process of creating individual KPI reports for our stakeholders.
links:
  lcc_2021:
    title: Leeds City Council KPI Report 2021/22
    link: ~/report/leeds-city-council-2021-2022.njk
---

The LEEDS 2023 team have to periodically create KPI (Key Performance Indicator) reports for our stakeholders,
whether funders, trustees or other interested parties. This project is focussed on automating the process of
creating and presenting these reports, ideally with no manual processing.

These reports will be in a similar style to [Open Innovations’ sponsor reviews][OI_REVIEW], presenting the key
metrics and narrative that are important to each stakeholder. 

[OI_REVIEW]: https://open-innovations.org/services/sponsors/reports/2021/

We will start with Leeds City Council, the KPIs for which are as follows: 

* Create job opportunities for at least 200 artists in the city 
* Employ, directly or indirectly through procurement, at least 50 people in the city 
* Secure at least 2 skills partnerships (with business/HEIs and/or others) to develop a skills programme for young people in the city
* Increase media coverage of LEEDS 2023 by at least 10% 
* Increase digital audiences by at least 10% 

## Data

The table below shows each of the above KPIs, the data sources used to evaluate them and the current values reported by LEEDS 2023 as of March 2022. 

  KPI         |  Data Source (TBC)
:------------:|:------------------:
Create job opportunities for at least 200 artists in the city | Excel spreadsheets manually created by LEEDS 2023
Employ, directly or indirectly through procurement, at least 50 people in the city | Excel spreadsheets manually created by LEEDS 2023
Secure at least 2 skills partnerships (with business/HEIs and/or others) to develop a skills programme for young people in the city | Excel spreadsheets manually created by LEEDS 2023
Increase media coverage of LEEDS 2023 by at least 10% | Data collected and maintained by Anita Morris Associates
Increase digital audiences by at least 10% | Google Analytics, Twitter API, Sprout social. Sprout social/combination of social media 

## Reports

{% comp "grid.autogrid" -%}
  {%- for id, link in links -%}
    {{- comp.grid.link({
      title: link.title,
      link: link.link | url
    }) | safe -}}
  {%- endfor -%}
{% endcomp %}
