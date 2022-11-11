const p = Deno.run({
  cmd: 'dvc dag --full --mermaid'.split(' '),
  stdout: 'piped',
});
export const pipelineDoc = new TextDecoder().decode(await p.output());
