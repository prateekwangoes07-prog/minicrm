# MiniCRM - UI Styling & Token Guidelines

This document details the interface guidelines and design tokens for MiniCRM. For general programming standards, check [MASTER_RULES.md](file:///c:/Users/User/OneDrive/Desktop/MiniCRM/docs/MASTER_RULES.md).

---

## 1. Color Palette Tokens

We use Tailwind variables to support unified styling:
* **Backgrounds**:
  * Default: `bg-slate-50` (light) / `bg-slate-950` (dark).
  * Containers/Cards: `bg-white` / `bg-slate-900`.
* **Borders**:
  * Clean division borders: `border-slate-200` (light) / `border-slate-800` (dark).
* **Text**:
  * Headings: `text-slate-900` / `text-slate-50`.
  * Secondary/Muted: `text-slate-500` / `text-slate-400`.
* **State Colors**:
  * Success: Green-based (e.g. `bg-green-50 text-green-700`).
  * Danger: Red-based (e.g. `bg-red-50 text-red-700`).

---

## 2. Typography Constraints

* **Font Family**: Sans-serif (using the Next.js `Geist` or system sans stack).
* **Sizes**:
  * Page Title: `text-2xl font-bold tracking-tight`.
  * Card Header: `text-base font-semibold`.
  * Body Text: `text-sm text-slate-600`.
  * Labels/Secondary: `text-xs text-slate-400`.

---

## 3. Layout Spacing Grid

We utilize an 8px (0.5rem) baseline spacing grid:
* **Padding (Card/Forms)**: `p-6` (24px) or `p-4` (16px).
* **Stacking Elements**: Use `space-y-4` (16px) or `space-y-6` (24px) for page forms.
* **Component Gaps**: Use `gap-2` (8px) for buttons, and `gap-4` (16px) for item grids.

---

## 4. Breakpoint Rules

* **Mobile (`sm`)**: Full-screen grid cards, hidden sidebar navigator.
* **Tablet (`md`)**: Mini-sidebar layouts.
* **Desktop (`lg` to `xl`)**: Sidebars locked open, grid views mapping to multi-column sections.
