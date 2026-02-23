# HTML Notebook Template Standard

Every module notebook is a **self-contained HTML file** — no build step, no bundler, opens in any browser.

## CDN Dependencies (pinned versions)

```html
<!-- Mermaid.js for diagrams -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {
      primaryColor: '#00A1E0',
      primaryTextColor: '#FFFFFF',
      primaryBorderColor: '#0078D4',
      lineColor: '#8B949E',
      secondaryColor: '#1A1F36',
      tertiaryColor: '#2D333B'
    }
  });
</script>

<!-- Prism.js for syntax highlighting -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/toolbar/prism-toolbar.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/toolbar/prism-toolbar.min.css"/>

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## Required Language Scripts for Prism

Always include autoloader which handles language loading. Key languages used in this course:
- `xml` (Mule XML flows)
- `yaml` (RAML specs)
- `python` (Flask mock, FastAPI, demo scripts)
- `json` (fixtures, payloads)
- `sql` (SOQL, PostgreSQL)
- `bash` (curl commands, shell)
- `csv` (test data)
- `java` (DataWeave — use `java` class as closest; or register custom)
- `properties` (application.properties)

For DataWeave: Prism has no native DataWeave support. Use `language-javascript` as a reasonable visual fallback, or define a custom grammar. Add a `data-label="DataWeave"` attribute on the `<pre>` tag for clarity.

## Color Palette

```css
:root {
  --sidebar-bg: #1A1F36;        /* Dark blue sidebar/header */
  --accent-primary: #00A1E0;    /* MuleSoft teal */
  --accent-secondary: #0078D4;  /* Darker blue for hover */
  --bg-main: #F8F9FA;           /* Light background */
  --bg-section: #FFFFFF;        /* White cards */
  --bg-lab: #F0F7FF;            /* Light blue lab sections */
  --bg-lab-advanced: #F5F0FF;   /* Light purple for advanced labs */
  --text-primary: #1A1F36;      /* Dark text */
  --text-secondary: #6B7280;    /* Gray secondary text */
  --border-light: #E5E7EB;      /* Light borders */
  --callout-info: #DBEAFE;      /* Blue info */
  --callout-success: #D1FAE5;   /* Green insight */
  --callout-warning: #FEF3C7;   /* Orange warning */
  --callout-danger: #FEE2E2;    /* Red anti-pattern */
  --callout-instructor: #EDE9FE; /* Purple instructor notes */
}
```

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module {N}: {Title} — MuleSoft Basics</title>
  <!-- CDN deps here -->
  <style>/* All CSS inline — self-contained */</style>
</head>
<body>
  <nav class="sidebar"><!-- Module navigation --></nav>
  <main class="content">
    <header class="module-header">
      <div class="badges">
        <span class="badge badge-duration">{Duration}</span>
        <span class="badge badge-day">Day {N}</span>
      </div>
      <h1>{Module Title}</h1>
      <p class="subtitle">{Subtitle}</p>
      <div class="objectives"><!-- Learning objectives --></div>
    </header>
    <!-- Sections -->
    <footer class="module-footer"><!-- Navigation links --></footer>
  </main>
</body>
</html>
```

## Typography

- **Headings**: `Inter`, weight 600-700
- **Body**: `Inter`, weight 400, **18px minimum** for projector readability
- **Code**: `JetBrains Mono`, weight 400-500, 15px
- Line height: 1.6 for body, 1.4 for code

## Component Patterns

### Callout Boxes

```html
<div class="callout callout-info">
  <div class="callout-title">Key Concept</div>
  <p>Content here</p>
</div>
<!-- Types: callout-info, callout-success, callout-warning, callout-danger -->
```

### Instructor Notes (Collapsible)

```html
<details class="instructor-note">
  <summary>Instructor Note</summary>
  <p>Content only the instructor sees when expanded.</p>
</details>
```

### Code Blocks (with copy button)

```html
<pre class="language-xml" data-label="Mule XML"><code class="language-xml">
&lt;flow name="example-flow"&gt;
  &lt;http:listener config-ref="HTTP_Listener" path="/api/test"/&gt;
&lt;/flow&gt;
</code></pre>
```

The toolbar plugin + copy-to-clipboard plugin auto-add copy buttons.

### Mermaid Diagrams

```html
<div class="diagram-container">
  <pre class="mermaid">
  graph TD
    A[System API] --> B[Process API]
    B --> C[Experience API]
  </pre>
  <p class="diagram-caption">Figure 1: API-Led Architecture</p>
</div>
```

### Lab Sections (distinct background)

```html
<section class="lab-section">
  <h2>Lab: {Title}</h2>
  <div class="lab-step">
    <div class="step-number">1</div>
    <div class="step-content">
      <h4>Step Title</h4>
      <p>Instructions...</p>
      <div class="validation">Validation: "Expected result description"</div>
    </div>
  </div>
</section>
```

### Comparison Tables

```html
<div class="comparison-table">
  <table>
    <thead><tr><th></th><th class="col-bad">Before</th><th class="col-good">After</th></tr></thead>
    <tbody>...</tbody>
  </table>
</div>
```

### Side-by-Side Code

```html
<div class="code-compare">
  <div class="code-panel code-panel-before">
    <h4>Python Script</h4>
    <pre class="language-python"><code>...</code></pre>
  </div>
  <div class="code-panel code-panel-after">
    <h4>DataWeave</h4>
    <pre class="language-javascript" data-label="DataWeave"><code>...</code></pre>
  </div>
</div>
```

## Responsive Rules

- Max content width: 900px centered
- Sidebar collapses on screens < 1024px
- Code blocks horizontally scroll, never wrap
- Tables horizontally scroll on mobile
- Font size never below 16px on mobile

## Validation Checklist for Every Notebook

1. Opens in browser with no console errors
2. All Mermaid diagrams render (no raw text visible)
3. All Prism code blocks are syntax-highlighted
4. Copy buttons work on all code blocks
5. Collapsible `<details>` sections open/close
6. Lab section has distinct background color
7. All links are relative or to known CDNs
8. No external images — use Mermaid or inline SVG only
9. Readable at 18px+ on a projector
10. Navigation footer links to adjacent modules
