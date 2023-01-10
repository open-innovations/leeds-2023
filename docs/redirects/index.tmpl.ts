export const layout="layouts/redirect.njk";

interface RedirectConfig {
  url: string;
  redirectTarget: string;
}

export default function* ({ redirects }: { redirects: RedirectConfig[] }) {
  for (const redirect of redirects) yield redirect;
}
