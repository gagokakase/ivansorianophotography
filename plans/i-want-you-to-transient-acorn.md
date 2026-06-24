# Ivan Soriano Photography — Premium Portfolio Website

## Context

The user wants a premium UX/UI design for Ivan Soriano Photography, a Filipino photography business based in Cavite, Philippines, specializing in weddings, debuts, and events.

**Brand Identity extracted from images + Facebook page:**
- Logo: Geometric 4-quadrant pinwheel mark (alternating forest-green/white quadrants with curved corners) + "IVAN SORIANO PHOTOGRAPHY" in elegant serif
- Brand color: Deep forest green (#1F4830 / #2D5A3D) + cream/white
- **Tagline**: "Moments that matters"
- **Services**: Weddings · Debuts & Cotillion · Events (Gala, Annual Parties, Adult Birthdays)
- **Location**: Cavite, Philippines
- **Contact**: 0936 288 6643 · ivp.photos@gmail.com · Ivan Soriano Photography (FB)
- **Featured work**: "The Wedding of Mark & Dianne", "Leorah Debut | Same Day Edit"
- Photography specialties: Wedding photography (Philippine heritage churches — Intramuros, Manila), portrait/fashion photography with dramatic lighting, debut/cotillion shoots

---

## Design System

### Color Palette
| Token | Value | Use |
|-------|-------|-----|
| `--brand-green` | `#1F4830` | Primary brand, nav, accents |
| `--brand-green-light` | `#2D5A3D` | Hover states, logo bg |
| `--brand-cream` | `#F2EDE4` | Headings on dark, body text |
| `--brand-gold` | `#C8A96E` | Accent line, CTA hover |
| `--bg-dark` | `#080C09` | Page background |
| `--bg-card` | `#111714` | Card/section backgrounds |

### Typography (via Google Fonts in fonts.css)
- **Display**: `Cormorant Garamond` — hero headings, section titles (elegant serif matching logo)
- **Body**: `Inter` — nav, body text, CTAs

### Design Language
- Dark, moody, editorial premium aesthetic
- Subtle grain texture overlay on hero
- Thin gold accent lines as dividers
- Full-bleed imagery
- Generous white-space
- Smooth scroll animations via `motion/react`

---

## Architecture

### Single-page scroll site with these sections:

1. **Navbar** — Fixed, glass-morphism on scroll: logo left, nav links center/right, "Book Now" CTA button
2. **Hero** — Full-screen (`100vh`) with wedding couple image (image-1.png), parallax-style, large serif headline, scroll indicator
3. **Services** — 3-column cards: Weddings | Debuts & Cotillion | Events (Gala, Parties, Birthdays). Each with an icon, short description, and hover reveal
4. **Portfolio Gallery** — Masonry-style editorial grid using `react-responsive-masonry`. 4 provided images + 2 Unsplash placeholders for completeness
5. **About** — Split layout: left = large photo placeholder, right = brand story, stats (years exp, weddings shot, cities)
6. **Testimonials** — Horizontal scroll carousel with 3 client quotes
7. **Contact / Book** — Two-column: left tagline + details, right form (name, email, event type, date, message) using `react-hook-form`
8. **Footer** — Logo, nav links, social icons (Facebook, Instagram), copyright

---

## Files to Create / Modify

### Modify
- `src/app/App.tsx` — Main entry, import all sections, set up scroll behavior
- `src/styles/theme.css` — Add brand color tokens
- `src/styles/fonts.css` — Add Cormorant Garamond + Inter Google Font imports

### Create
- `src/app/components/Navbar.tsx`
- `src/app/components/HeroSection.tsx`
- `src/app/components/ServicesSection.tsx`
- `src/app/components/PortfolioSection.tsx`
- `src/app/components/AboutSection.tsx`
- `src/app/components/TestimonialsSection.tsx`
- `src/app/components/ContactSection.tsx`
- `src/app/components/Footer.tsx`
- `src/app/components/LogoMark.tsx` — SVG recreation of the 4-quadrant brand mark

---

## Key Implementation Details

### Logo Mark (SVG)
Recreate the 4-quadrant pinwheel from image.png as inline SVG:
- 2×2 grid of squares with circular arc cutouts alternating between forest-green fill and white fill
- Placed in Navbar and Footer

### Hero Section
- Full-viewport with `image-1.png` (wedding couple at colonial church) as background
- Dark gradient overlay (bottom-to-top, 60% opacity)
- Headline: "Capturing Love Stories" in Cormorant Garamond 96px
- Sub: "Wedding & Portrait Photography · Philippines"
- Two CTAs: "View Portfolio" (outlined) + "Book a Session" (filled green)
- Animated scroll-down chevron

### Portfolio Grid
Import all 4 sample images from `src/imports/`:
```tsx
import img1 from "../imports/image-1.png"  // wedding exterior
import img2 from "../imports/image-2.png"  // portrait red
import img3 from "../imports/image-3.png"  // groom church
import img4 from "../imports/image-4.png"  // bride church
```
Use `react-responsive-masonry` for asymmetric grid. Hover overlay shows category label.

### Contact Form
Use `react-hook-form` v7.55.0 (already installed). Fields: name, email, phone, event type (select: Wedding / Debut & Cotillion / Events), event date, message.
Real contact details in the section: **0936 288 6643**, **ivp.photos@gmail.com**, Location: **Cavite, Philippines**.
Submit shows success toast via `sonner`.

### Animations
- `motion/react` for section fade-in-up on scroll (`whileInView`)
- Navbar background transition on scroll via `useEffect` + `scrollY`

---

## Verification

1. All 4 sample images appear correctly in the portfolio grid
2. Logo mark renders in nav and footer
3. Navbar glass effect activates on scroll past hero
4. Contact form validates and shows success toast
5. All sections are reachable via nav links (smooth scroll)
6. Responsive: hamburger menu on mobile, single-column stacks
