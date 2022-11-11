// const p = Deno.run({
//   cmd: 'dvc dag --full --mermaid'.split(' '),
//   stdout: 'piped',
// });
// export const pipelineDoc = new TextDecoder().decode(await p.output());
export const pipelineDoc = `flowchart TD
  node1["scripts/metrics/ballot/dvc.yaml:stage_build"]
  node2["scripts/metrics/ballot/dvc.yaml:summarise"]
  node3["scripts/metrics/callouts/dvc.yaml:build"]
  node4["scripts/metrics/callouts/dvc.yaml:stage"]
  node5["scripts/reference_data/dvc.yaml:postcodes"]
  node6["working/ref/onspd-extract.csv.dvc"]
  node1-->node2
  node4-->node3
  node5-->node1
  node5-->node3
  node6-->node5

`
