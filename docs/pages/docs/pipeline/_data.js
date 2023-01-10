// const p = Deno.run({
//   cmd: 'dvc dag --full --mermaid'.split(' '),
//   stdout: 'piped',
// });
// export const pipelineDoc = new TextDecoder().decode(await p.output());
export const pipelineDoc = `flowchart LR
  node6["scripts/metrics/callouts/dvc.yaml:extract"]
  node9["scripts/metrics/roadshows/dvc.yaml:extract"]
  node18["working/ref/onspd-extract.csv.dvc"]
  node23["working/manual/fundraising.dvc"]

  node17["working/metrics/rosterfy.dvc"]
  node13["scripts/metrics/volunteers/dvc.yaml:prepare"]
  node14["scripts/metrics/volunteers/dvc.yaml:transform"]

  node27["working/manual/media.dvc"]
  node24["scripts/metrics/media_coverage/dvc.yaml:prepare"]
  node25["scripts/metrics/media_coverage/dvc.yaml:transform"]
  node26["scripts/metrics/media_coverage/dvc.yaml:transform_historic"]

  node28["working/manual/mwmcmn.dvc"]
  node29["scripts/metrics/activity/dvc.yaml:transform"]

  node30["working/manual/activity/Leeds_2023_activity_logging_MASTER.xlsx.dvc"]

  node1["scripts/dashboard/community/dvc.yaml:prepare_events"]
  node2["scripts/dashboard/community/dvc.yaml:prepare_residents"]
  node3["scripts/metrics/ballot/dvc.yaml:extract"]
  node4["scripts/metrics/ballot/dvc.yaml:prepare"]
  node5["scripts/metrics/ballot/dvc.yaml:transform"]
  node7["scripts/metrics/callouts/dvc.yaml:prepare"]
  node8["scripts/metrics/callouts/dvc.yaml:transform"]
  node10["scripts/metrics/roadshows/dvc.yaml:prepare"]
  node11["scripts/metrics/roadshows/dvc.yaml:transform"]
  node12["scripts/metrics/schools/dvc.yaml:transform"]
  node15["scripts/reference_data/dvc.yaml:postcodes"]
  node16["working/manual/schools.dvc"]
  node19["working/roadshow/Leeds_2023_Roadshow_Open_Innovations.xlsx.dvc"]
  node20["working/manual/social.dvc"]
  node21["scripts/metrics/fundraising/dvc.yaml:prepare"]
  node22["scripts/metrics/fundraising/dvc.yaml:transform"]
  
  

  node3-->node5
  node5-->node2
  node5-->node4
  node6-->node8
  node8-->node7
  node9-->node11
  node10-->node2
  node11-->node1
  node11-->node10
  node12-->node1
  node12-->node2
  node14-->node2
  node14-->node13
  node15-->node3
  node15-->node5
  node15-->node8
  node15-->node11
  node16-->node12
  node17-->node14
  node18-->node15
  node19-->node11
  node22-->node21
  node23-->node22
  node25-->node24
  node26-->node24
  node27-->node25
  node27-->node26
  node30-->node29

`;
