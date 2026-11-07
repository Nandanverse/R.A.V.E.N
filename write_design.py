import pathlib
content = """# RAVEN Design System

This document defines the complete design system for RAVEN. All visual and interaction decisions must conform to this specification.

---

## Design Philosophy

RAVEN is a cybersecurity engineering tool. Its interface must communicate:

- **Precision** - Every pixel serves a purpose. No decoration.
- **Trustworthiness** - Consistent, predictable behavior. No surprises.
- **Density** - Information-rich without clutter. High data-to-ink ratio.
- **Accessibility** - Usable by security professionals with diverse needs.
- **Seriousness** - Visual language matches the domain: security operations, not SaaS marketing.

---

## Prohibited Visual Effects

The following are **strictly prohibited** across the entire application:

| Prohibited | Reason |
|------------|--------|
| Gradients | Adds visual noise, reduces contrast, looks like marketing |
| Emojis | Unprofessional, inconsistent rendering, accessibility issues |
| Decorative colored borders | False affordance, distracts from actual status indicators |
| Box shadows | Adds depth illusion, conflicts with flat technical aesthetic |
| Glassmorphism / frosted glass | Reduces legibility, performance cost, trendy not timeless |
| Glowing effects | Distracting, implies state changes that do not exist |
| Excessive rounded cards | Reduces information density, looks consumer-oriented |
| Animated backgrounds | CPU waste, distraction, accessibility violation |
| On-hover movement (translate, scale, bounce, slide) | False affordance, breaks spatial memory, vestibular issues |
| Unnecessary transitions | Slows perceived performance, adds complexity |
| Decorative AI-generated illustrations | No informational value, increases bundle size |
| Excessive empty dashboard cards | Wastes space, implies missing functionality |
| Fake activity feeds / fabricated findings | Destroys trust, professionally unethical |

**Enforcement**: CI includes a visual regression check that fails on detected gradients, shadows, or animations in production builds.

---

## Color Palette

### Neutral Scale (Primary)

```css
/* Backgrounds */
--bg-base: #0d0d0d;        /* Primary background */
--bg-elevated: #141414;    /* Cards, panels, modals */
--bg-hover: #1a1a1a;       /* Row hover, button hover */
--bg-active: #222222;      /* Active/pressed states */
--bg-border: #2a2a2a;      /* Borders, dividers */

/* Text */
--fg-primary: #e8e8e8;     /* Primary text */
--fg-secondary: #a0a0a0;   /* Secondary text, labels */
--fg-muted: #6a6a6a;       /* Placeholders, disabled text */
--fg-inverse: #0d0d0d;     /* Text on colored backgrounds */

/* Monospace (technical data) */
--fg-mono: #d4d4d4;        /* IP addresses, ports, hashes, commands */
--bg-mono: #111111;        /* Inline code, code blocks */
```

### Semantic Colors (Security States Only)

Color is **only** used for actual security states. Never for decoration.

```css
/* Severity - mapped to CVSS */
--sev-critical: #dc2626;   /* CVSS 9.0-10.0 */
--sev-high: #ea580c;       /* CVSS 7.0-8.9 */
--sev-medium: #ca8a04;     /* CVSS 4.0-6.9 */
--sev-low: #16a34a;        /* CVSS 0.1-3.9 */
--sev-info: #2563eb;       /* Informational */
--sev-none: #525252;       /* No severity / cleared */

/* Status */
--status-success: #16a34a; /* Validated, passed, complete */
--status-warning: #ca8a04; /* Pending, needs review */
--status-danger: #dc2626;  /* Failed, critical, blocked */
--status-info: #2563eb;    /* Running, in progress */
--status-neutral: #525252; /* Idle, unknown, neutral */

/* Validation States */
--validated: #16a34a;      /* Confirmed vulnerability */
--suspected: #ca8a04;      /* Scanner-reported, not validated */
--rejected: #dc2626;       /* False positive / rejected */
--pending: #2563eb;        /* Awaiting validation */
```

### Usage Rules

1. **Never** use semantic colors for non-security UI (e.g., navigation, buttons, headers).
2. **Never** mix semantic colors (e.g., critical border on a medium card).
3. **Always** pair color with text/icon for accessibility (never color-only).
4. **Backgrounds** remain neutral. Semantic colors appear only on: badges, status dots, severity columns, graph nodes, inline indicators.

---

## Typography

### Font Stack

```css
/* UI Text - System font for performance and native feel */
--font-ui: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* Monospace - Technical data, code, commands */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', monospace;

/* Headings - Same as UI but tracked tighter */
--font-heading: var(--font-ui);
```

### Type Scale

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| --text-xs | 11px | 400 | 1.4 | +0.02em | Timestamps, footnotes, badges |
| --text-sm | 12px | 400 | 1.5 | 0 | Secondary labels, table cells |
| --text-base | 13px | 400 | 1.5 | 0 | Body text, form inputs |
| --text-lg | 14px | 500 | 1.4 | -0.01em | Emphasized body, card titles |
| --text-xl | 16px | 600 | 1.3 | -0.02em | Section headers |
| --text-2xl | 20px | 600 | 1.2 | -0.02em | Page titles |
| --text-3xl | 28px | 700 | 1.1 | -0.03em | Dashboard hero numbers |

### Monospace Scale

| Token | Size | Usage |
|-------|------|-------|
| --mono-xs | 10px | Inline hashes, short IDs |
| --mono-sm | 11px | IP addresses, ports, CVEs in tables |
| --mono-base | 12px | Commands, JSON, code blocks |
| --mono-lg | 13px | Terminal output, logs |

### Rules

- **All technical identifiers** (IPs, ports, CVEs, hashes, commands, JSON keys) use monospace.
- **Never** use monospace for body prose.
- **Headings** use --font-heading at --text-xl or larger.
- **Tables** use --text-sm for cells, --mono-sm for technical columns.

---

## Spacing

### Base Unit: 4px

All spacing values are multiples of 4px.

```css
--space-0: 0;
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

### Application

| Context | Spacing |
|---------|---------|
| Component internal padding | --space-4 (16px) |
| Section vertical gap | --space-6 (24px) |
| Page section gap | --space-8 (32px) |
| Inline element gap | --space-2 (8px) |
| Form field gap | --space-4 (16px) |
| Table cell padding | --space-2 --space-3 (8px 12px) |
| Sidebar item padding | --space-3 --space-4 (12px 16px) |

---

## Layout

### Application Shell

```
+-----------------------------------------------------------------+
|  Header (48px) - App title, global actions, user menu           |
+----------+------------------------------------------------------+
|          |                                                      |
|  Sidebar |  Main Content                                        |
|  (260px) |  (flex-1, min-width 0)                               |
|          |                                                      |
|  Nav     |  Page Header (optional)                              |
|  Modules |  +----------------------------------------------+   |
|          |  | Content Area                                  |   |
|          |  | (responsive grid / flex)                     |   |
|          |  +----------------------------------------------+   |
|          |                                                      |
+----------+------------------------------------------------------+
|  Footer (optional, 32px) - Status bar, version, shortcuts       |
+-----------------------------------------------------------------+
```

### Breakpoints

```css
--bp-sm: 640px;   /* Mobile - sidebar collapses to drawer */
--bp-md: 1024px;  /* Tablet - 2-column grids */
--bp-lg: 1280px;  /* Desktop - full sidebar, 3-column grids */
--bp-xl: 1536px;  /* Wide - 4-column analytics grids */
```

### Grid System

- 12-column fluid grid (CSS Grid)
- Gap: --space-4 (16px)
- Container max-width: none (full viewport)
- Content areas use min-width: 0 to prevent overflow

---

## Sidebar Navigation

### Structure

```tsx
<nav role="navigation" aria-label="Main navigation">
  <ul className="nav-list">
    <li><NavLink to="/overview">Overview</NavLink></li>
    <li><NavLink to="/assessments">Assessments</NavLink></li>
    <li><NavLink to="/assets">Asset Inventory</NavLink></li>
    <li><NavLink to="/recon">Reconnaissance</NavLink></li>
    <li><NavLink to="/intel">Vulnerability Intelligence</NavLink></li>
    <li><NavLink to="/findings">Findings</NavLink></li>
    <li><NavLink to="/attack-graph">Attack Graph</NavLink></li>
    <li><NavLink to="/ai">AI Analysis</NavLink></li>
    <li><NavLink to="/analytics">Analytics</NavLink></li>
    <li><NavLink to="/reports">Reports</NavLink></li>
    <li><NavLink to="/settings">Settings</NavLink></li>
    <li><NavLink to="/about">About</NavLink></li>
  </ul>
</nav>
```

### Visual Spec

- Width: 260px (collapsed: 64px icon-only)
- Background: --bg-elevated
- Border-right: 1px solid --bg-border
- Items: --text-sm --fg-primary, padding --space-3 --space-4
- Active: --bg-hover background, 2px left border --sev-info
- Hover: --bg-hover background (no transform, no transition)
- Icons: Lucide, 18x18px, --fg-secondary
- Collapsed tooltip: native browser tooltip (no custom tooltip component)

### Mobile (< 640px)

- Sidebar becomes fixed drawer (z-index 50)
- Hamburger button in header (aria-label="Open navigation")
- Backdrop overlay on open
- Swipe-to-close supported

---

## Navigation Patterns

### Page Header

```tsx
<header className="page-header">
  <div className="page-title-group">
    <h1 className="page-title">Page Title</h1>
    <p className="page-description">Optional description</p>
  </div>
  <div className="page-actions">
    <Button variant="primary">Primary Action</Button>
    <Button variant="secondary">Secondary</Button>
  </div>
</header>
```

- Height: auto, minimum 56px
- Border-bottom: 1px solid --bg-border
- Padding: --space-4 --space-6

### Breadcrumbs (when depth > 1)

```tsx
<nav aria-label="Breadcrumb">
  <ol className="breadcrumbs">
    <li><Link to="/">Home</Link></li>
    <li><Link to="/assessments">Assessments</Link></li>
    <li aria-current="page">Assessment #123</li>
  </ol>
</nav>
```

- Separator: / in --fg-muted
- Current page: --fg-secondary, not a link

---

## Tables

### Structure

```tsx
<table className="data-table" role="grid">
  <thead>
    <tr>
      <th scope="col">Column</th>
      <th scope="col"><span className="sr-only">Actions</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code className="mono">192.168.1.1</code></td>
      <td><Button variant="ghost" size="sm">View</Button></td>
    </tr>
  </tbody>
</table>
```

### Visual Spec

| Property | Value |
|----------|-------|
| Background | --bg-base |
| Header background | --bg-elevated |
| Header text | --fg-secondary, --text-xs, uppercase, tracking +0.05em |
| Row border-bottom | 1px solid --bg-border |
| Row hover | --bg-hover (no transition) |
| Cell padding | --space-2 --space-3 |
| Technical columns | --mono-sm --fg-mono |
| Severity badge | Inline, see Badge component |
| Sortable header | cursor: pointer, sort icon --fg-muted |

### Responsive

- < 640px: Horizontal scroll on table wrapper, sticky first column
- < 1024px: Hide low-priority columns (configurable per table)

---

## Forms

### Field Structure

```tsx
<div className="form-field">
  <label htmlFor="target" className="form-label">Target</label>
  <input
    id="target"
    type="text"
    className="form-input"
    placeholder="example.com"
    aria-describedby="target-hint"
  />
  <p id="target-hint" className="form-hint">FQDN or CIDR notation</p>
  <p className="form-error" role="alert">Error message</p>
</div>
```

### Visual Spec

| Element | Spec |
|---------|------|
| Label | --text-sm --fg-primary, --font-ui, margin-bottom --space-1 |
| Input | --bg-elevated, border 1px --bg-border, --text-base --fg-primary, padding --space-2 --space-3, radius 4px |
| Input:focus | Border --sev-info, outline none, ring 2px --sev-info at 20% opacity |
| Input:invalid | Border --status-danger |
| Input:disabled | --bg-border, --fg-muted, cursor not-allowed |
| Placeholder | --fg-muted |
| Hint | --text-xs --fg-secondary |
| Error | --text-xs --status-danger, icon left |

### Input Variants

- **Text**: Standard
- **Select**: Native <select> styled to match input
- **Textarea**: Min-height 100px, resize vertical
- **Checkbox/Radio**: Custom styled, 16x16px, focus ring
- **Toggle**: For boolean settings, accessible switch pattern

---

## Buttons

### Variants

| Variant | Background | Text | Border | Usage |
|---------|------------|------|--------|-------|
| primary | --sev-info | --fg-inverse | none | Main action per page |
| secondary | --bg-hover | --fg-primary | 1px --bg-border | Secondary actions |
| ghost | transparent | --fg-secondary | none | Toolbar, low-emphasis |
| danger | --status-danger | --fg-inverse | none | Destructive actions |
| success | --status-success | --fg-inverse | none | Confirm positive actions |

### Sizes

| Size | Padding | Font | Height |
|------|---------|------|--------|
| sm | --space-1 --space-3 | --text-xs | 28px |
| md | --space-2 --space-4 | --text-sm | 36px |
| lg | --space-3 --space-6 | --text-base | 44px |

### States

- **Default**: As defined above
- **Hover**: --bg-hover for secondary/ghost; 10% darker for primary/danger/success (no transform)
- **Active**: --bg-active background
- **Focus**: 2px ring --sev-info at 20% opacity, offset 2px
- **Disabled**: --bg-border bg, --fg-muted text, cursor not-allowed
- **Loading**: Spinner (16px) replaces text, width locked

### Icon Buttons

- Square: 32x32px (md), 28x28px (sm), 40x40px (lg)
- Icon centered, --fg-secondary default, --fg-primary hover
- Aria-label required

---

## Status Indicators

### Badge

```tsx
<Badge variant="critical">Critical</Badge>
<Badge variant="validated">Validated</Badge>
<Badge variant="pending">Pending</Badge>
```

| Variant | Background | Text | Border |
|---------|------------|------|--------|
| critical | --sev-critical at 15% | --sev-critical | 1px --sev-critical at 30% |
| high | --sev-high at 15% | --sev-high | 1px --sev-high at 30% |
| medium | --sev-medium at 15% | --sev-medium | 1px --sev-medium at 30% |
| low | --sev-low at 15% | --sev-low | 1px --sev-low at 30% |
| info | --sev-info at 15% | --sev-info | 1px --sev-info at 30% |
| validated | --validated at 15% | --validated | 1px --validated at 30% |
| suspected | --suspected at 15% | --suspected | 1px --suspected at 30% |
| rejected | --rejected at 15% | --rejected | 1px --rejected at 30% |
| pending | --pending at 15% | --pending | 1px --pending at 30% |
| neutral | --bg-hover | --fg-secondary | 1px --bg-border |

- Size: --text-xs, padding --space-1 --space-2, radius 4px
- Never animated

### Status Dot

```tsx
<StatusDot status="running" />
<StatusDot status="success" />
<StatusDot status="danger" />
```

- 8x8px circle, border-radius 50%
- No pulse, no animation
- Tooltip on hover with full status text

---

## Charts

### Library: Plotly.js (via react-plotly.js)

### Style Rules

- Background: --bg-elevated
- Grid lines: --bg-border (thin, 0.5px)
- Axis lines: --bg-border
- Axis labels: --fg-secondary --text-xs
- Tick labels: --fg-muted --text-xs
- Series colors: Use semantic severity palette only
- Legend: --fg-secondary --text-sm, bottom or right
- Tooltip: --bg-elevated, border --bg-border, --fg-primary
- No animations on initial render or hover
- Responsive: useResizeHandler true, static plot for exports

### Chart Types by Data

| Data | Chart Type |
|------|------------|
| Vulnerability distribution | Horizontal bar (stacked by validation status) |
| Severity over time | Line (step interpolation) |
| Asset exposure | Treemap (area = criticality) |
| Tool success rates | Grouped bar |
| Attack path depth | Histogram |

---

## Graph Visualization (Attack Graph)

### Library: Cytoscape.js

### Style Rules

- Background: --bg-base
- Node base: --bg-elevated, border 1px --bg-border, 4px radius
- Node sizes: Asset 40px, Service 32px, Vulnerability 28px, Finding 24px
- Node colors: By type (neutral), severity border for vulns/findings
- Edge: 1.5px --fg-muted, curved (bezier), arrow on target
- Edge labels: --text-xs --fg-muted, background --bg-elevated padded
- Selection: 2px ring --sev-info, z-index elevated
- Hover: Highlight connected edges/nodes (no movement)
- Layout: cose-bilkent for organic, dagre for hierarchical
- Pan/zoom: Enabled, wheel zoom, pinch zoom
- Export: PNG (3x), SVG

### Node Data Attributes

```ts
interface GraphNode {
  id: string;
  type: 'asset' | 'service' | 'vulnerability' | 'finding';
  label: string;
  severity?: 'critical' | 'high' | 'medium' | 'low' | 'info';
  validated?: boolean;
  evidenceCount?: number;
  metadata: Record<string, unknown>;
}
```

---

## Responsive Behavior

### Sidebar

| Breakpoint | Behavior |
|------------|----------|
| > 1024px | Full sidebar (260px) |
| 768px - 1024px | Collapsed icon-only (64px), hover expands |
| < 768px | Drawer overlay, hamburger menu |

### Tables

| Breakpoint | Behavior |
|------------|----------|
| > 1024px | All columns visible |
| 768px - 1024px | Hide description, metadata columns |
| < 768px | Horizontal scroll, sticky first 2 columns |

### Grids

| Breakpoint | Columns |
|------------|---------|
| > 1280px | 4 (analytics), 3 (cards) |
| 1024px - 1280px | 3 (analytics), 2 (cards) |
| 768px - 1024px | 2 (analytics), 1 (cards) |
| < 768px | 1 (all) |

### Modals/Drawers

- Mobile: Full-screen drawer from bottom
- Desktop: Centered modal, max-width 640px (forms), 900px (detail)

---

## Accessibility

### Minimum Requirements (WCAG 2.1 AA)

- **Contrast**: All text 4.5:1, large text 3:1, UI components 3:1
- **Focus**: Visible focus indicator on all interactive elements (2px ring, offset 2px)
- **Keyboard**: All functionality operable via keyboard alone
- **Screen readers**: Semantic HTML, ARIA labels where needed, live regions for status
- **Reduced motion**: @media (prefers-reduced-motion: reduce) disables all transitions/animations
- **Zoom**: Functional at 200% browser zoom
- **Color blindness**: Never color-only status; always icon + text + color

### Implementation Checklist

- [ ] skip-link at top of body
- [ ] lang attribute on <html>
- [ ] Heading hierarchy (h1 to h2 to h3) never skipped
- [ ] aria-label on icon-only buttons
- [ ] aria-describedby on inputs with hints/errors
- [ ] role="alert" on live error messages
- [ ] aria-live="polite" on status updates
- [ ] Table headers with scope="col"
- [ ] Focus trap in modals/drawers
- [ ] Escape key closes modals/drawers

---

## Component Rules

### Animate UI Usage

Animate UI components are permitted **only** in these static configurations:

| Component | Configuration |
|-----------|---------------|
| Card | Static, no hover lift, no entrance animation |
| Button | Static, no press animation, no loading spinner animation (use CSS spinner) |
| Badge | Static |
| Table | Static, no row animation |
| Tabs | Static, no slide indicator |
| Select | Static dropdown, no animation |
| Tooltip | Static, position: absolute, no fade |
| Dropdown | Static, no slide/fade |
| Modal / Drawer | Static appear, no slide/fade |
| Progress | Static bar, no indeterminate animation |
| Spinner | CSS-only rotation (respects prefers-reduced-motion) |

**Prohibited Animate UI features**: motion, animate, initial, exit, transition, whileHover, whileTap, whileFocus, layout, animatePresence.

### Custom Component Patterns

When Animate UI cannot meet restrictions, implement static alternatives:

```tsx
// Instead of Animate UI Card with hover lift
export function Card({ children, className }) {
  return (
    <div className={cn('bg-bg-elevated border border-bg-border rounded-lg', className)}>
      {children}
    </div>
  );
}

// Instead of Animate UI Button with press scale
export function Button({ children, variant = 'secondary', ...props }) {
  const base = 'inline-flex items-center justify-center font-medium rounded-md transition-none';
  const variants = {
    primary: 'bg-sev-info text-fg-inverse hover:bg-sev-info/90',
    secondary: 'bg-bg-hover text-fg-primary border border-bg-border hover:bg-bg-active',
    # ...
  };
  return <button className={cn(base, variants[variant])} {...props}>{children}</button>;
}
```

### Component Checklist

Every component must:
- [ ] Use design tokens (no hardcoded colors/spacing)
- [ ] Support className prop for composition
- [ ] Forward ref (use forwardRef)
- [ ] Have TypeScript interface for props
- [ ] Include JSDoc with usage example
- [ ] Test: render, focus, keyboard, screen reader

---

## Design Tokens (CSS Custom Properties)

```css
:root {
  /* Color - Neutral */
  --bg-base: #0d0d0d;
  --bg-elevated: #141414;
  --bg-hover: #1a1a1a;
  --bg-active: #222222;
  --bg-border: #2a2a2a;
  --fg-primary: #e8e8e8;
  --fg-secondary: #a0a0a0;
  --fg-muted: #6a6a6a;
  --fg-inverse: #0d0d0d;
  --fg-mono: #d4d4d4;
  --bg-mono: #111111;

  /* Color - Semantic (Security Only) */
  --sev-critical: #dc2626;
  --sev-high: #ea580c;
  --sev-medium: #ca8a04;
  --sev-low: #16a34a;
  --sev-info: #2563eb;
  --sev-none: #525252;
  --status-success: #16a34a;
  --status-warning: #ca8a04;
  --status-danger: #dc2626;
  --status-info: #2563eb;
  --status-neutral: #525252;
  --validated: #16a34a;
  --suspected: #ca8a04;
  --rejected: #dc2626;
  --pending: #2563eb;

  /* Typography */
  --font-ui: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', monospace;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;

  /* Shadows (only for focus rings, not decorative) */
  --focus-ring: 0 0 0 2px var(--sev-info);
}
```

---

## Motion Restrictions Summary

| Feature | Allowed? | Notes |
|---------|----------|-------|
| CSS transition | No | Except focus ring (handled by browser) |
| CSS animation | No | Except spinner @keyframes spin |
| JS animation libraries | No | Framer Motion, etc. prohibited |
| Hover transform/scale | No | Breaks spatial consistency |
| Entrance/exit animations | No | Adds latency, accessibility issue |
| Loading skeletons | No | Use static placeholder text |
| Progress bar animation | No | Static fill |
| Tooltip fade | No | Instant show/hide |
| Modal slide/fade | No | Instant appear |
| Graph layout animation | No | Layout once on mount |
| Page transitions | No | Instant navigation |

**Exception**: The CSS spinner for loading buttons uses @keyframes spin but is wrapped in @media (prefers-reduced-motion: no-preference) so it respects user preference.

---

## Implementation Priority

1. **Tokens** - Define in frontend/src/styles/tokens.css, import at root
2. **Base** - Reset, typography, focus styles in frontend/src/styles/global.css
3. **Primitives** - Button, Input, Badge, Table, Card in frontend/src/components/ui/
4. **Layout** - Shell, Sidebar, Header in frontend/src/components/layout/
5. **Patterns** - Forms, Tables, Lists in frontend/src/components/patterns/
6. **Features** - Page-specific components in frontend/src/features/
7. **Pages** - Compose features in frontend/src/pages/

---

## Verification

```bash
# Visual regression (chromatic or similar)
npm run test:visual

# Accessibility audit
npm run test:a11y

# Design token compliance
npm run lint:design-tokens

# Reduced motion check
npm run test:reduced-motion
```

All checks must pass in CI before merge."""
pathlib.Path("C:/Users/nanda/OneDrive/Desktop/RAVEN/design.md").write_text(content, encoding="utf-8")
print("done")
