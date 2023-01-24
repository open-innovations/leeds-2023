import values from "../../_data/headlines/values.js";

const metricHeadlingStyle = `
  :host { --font-size: 4em; --impact-fontstack: unset; --block-colour: #aaa; }
  .metric { display: block; width: auto; background: var(--block-colour); padding: 1em; }
  .metric > * { text-align: center; }
  .big-number { font-weight: bold; font-size: var(--font-size); font-family: var(--impact-fontstack); }
`;

class MetricHeadline extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
    // write element functionality in here
  }
  connectedCallback() {
    const topic = this.getAttribute("data-topic");
    const metric = this.getAttribute("data-metric");
    const impactFontstack = this.getAttribute("data-impact-font") || 'unset';
    const blockColour = this.getAttribute("data-colour") || 'unset';

    if (topic === null) throw new Error('No "data-topic" attribute provided');
    if (metric === null) throw new Error('No "data-metric" attribute provided');
    if (!Object.hasOwn(values, topic)) throw new Error(`data-topic "${topic}" is not known`);
    if (!Object.hasOwn((<Record<string, Record<string, unknown>>>values)[topic], metric)) throw new Error(`data-topic "${topic}" has no data-metric called "${metric}"`);

    const value = (<Record<string, Record<string, number>>>values)[topic][metric];

    // Create a shadow root
    this.attachShadow({ mode: "open" }); // sets and returns 'this.shadowRoot'

    // Create (nested) span elements
    const wrapper = document.createElement("div");
    wrapper.setAttribute("class", "metric");
    wrapper.setAttribute("style", `--impact-fontstack:${impactFontstack};--block-colour:${blockColour};`);

    if (this.hasAttribute("data-header-text")) {
      const header = document.createElement("div");
      header.innerText = this.getAttribute("data-header-text") || "";
      wrapper.append(header);
    }

    const number = document.createElement("div");
    number.classList.add('big-number');
    number.innerText = value.toLocaleString();
    wrapper.append(number);

    if (this.hasAttribute("data-footer-text")) {
      const footer = document.createElement("div");
      footer.innerText = this.getAttribute("data-header-text") || "";
      wrapper.append(footer);
    }

    // Create some CSS to apply to the shadow DOM
    const style = document.createElement("style");
    style.textContent = metricHeadlingStyle;

    // attach the created elements to the shadow DOM
    this.shadowRoot!.append(style, wrapper);
  }
}

customElements.define("metric-headline", MetricHeadline);