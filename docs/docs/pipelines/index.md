---
title: Pipeline diagrams
url: /docs/pipelines/
---

<style>
  .diagram span.nodeLabel {
    font-size: 0.9em;
  }
</style>

The site uses [DVC](https://dvc.org/) to orchestrate the repeatable pipelines.

The diagrams below show the depedency graphs of the stages and output files.
These have been generated by the `dvc dag` command.

## Stages view

<img id='pipelines-stages' class='diagram'
  src='/assets/images/docs/pipelines-stages.svg' inline
  alt='A graph showing the stages for the data pipelines'>

## Outputs view

<img id='pipelines-files' class='diagram'
  src='/assets/images/docs/pipelines-files.svg' inline
  alt='A graph showing the input and output files for the data pipelines'>