---
title: Key Performance Indicator tracker
---
<style>
  table {
    border-collapse: collapse;
  }
  td, th {
    border: 1px solid lightgrey;
    padding: 0.4rem;
  }
  th {
    color: white;
    background: grey;
  }
</style>

As part of our work to demonstrate the value and impact of Leeds 2023, we will be producing a
series of interactive visualisations, roughly based on
[Open Innovations’ sponsor reviews][OI_REVIEW], that will present Leeds 2023’s progress
and achievement of its KPIs for some of its own sponsors and funders. 

[OI_REVIEW]: https://open-innovations.org/services/sponsors/reports/2021/

We will start with Leeds City Council, the KPIs for which are as follows: 

* Create job opportunities for at least 200 artists in the city 
* Employ, directly or indirectly through procurement, at least 50 people in the city 
* Secure at least 2 skills partnerships (with business/HEIs and/or others) to develop a skills programme for young people in the city
*&* Increase media coverage of LEEDS 2023 by at least 10% 
* Increase digital audiences by at least 10% 

## Data

The table below shows each of the above KPIs, the data sources used to evaluate them and the current values reported by Leeds 2023 as of March 2022. 

KPI | Data Source (TBC)
----|------------------
Create job opportunities for at least 200 artists in the city | Excel spreadsheets manually created by Leeds 2023
Employ, directly or indirectly through procurement, at least 50 people in the city | Excel spreadsheets manually created by Leeds 2023
Secure at least 2 skills partnerships (with business/HEIs and/or others) to develop a skills programme for young people in the city | Excel spreadsheets manually created by Leeds 2023
Increase media coverage of LEEDS 2023 by at least 10% | Data collected and maintained by Anita Morris Associates
Increase digital audiences by at least 10% | Google Analytics, Twitter API, Sprout social. Sprout social/combination of social media 

## Wireframe

The visualisation will ‘live’ on the Leeds 2023
microsite. 

As a first iteration we will pull together the
above data sources into a short report to
represent performance against the 5 KPIs.
This may progress into a more sophisticated
visualisation in later iterations, but
for now it will look roughly as follows: 

<style>
  .outlined {
    border: 5rem solid grey;
    padding: 1rem 3rem;
  }
</style>
<section class='outlined'>
{% include visualisations/kpi.html %}
</section>
