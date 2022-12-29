/**
    Custom element which is replaced by an altmetric donut and a link to the study
**/
class AltmetricElement extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        // Store and clear inner contents
        let content = this.innerHTML;
        this.innerHTML = "";
        // Make sure element has a position so sub-elements are positioned relative to it
        this.style.display = "grid";
        this.style.position = "relative";
        this.style.alignItems = "center";
        this.style.gridTemplateColumns = "[left] 5rem [mid] auto [right]";
        // Make donut
        this.badge = document.createElement("div");
        this.badge.style.position = 'relative';
        this.badge.className = 'altmetric-embed';
        this.badge.dataset.badgeType = 'donut';
        this.badge.dataset.doi = this.dataset.doi;
        this.appendChild(this.badge);
        // Make link
        this.citation = document.createElement("a");
        this.citation.innerHTML = content;
        this.citation.href = this.dataset.doi;
        this.appendChild(this.citation);
    }
}
document.addEventListener('DOMContentLoaded', function() {
    customElements.define('altmetric-embed', AltmetricElement);
})