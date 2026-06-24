import { LogoFull } from "./LogoMark";
import { Facebook, Instagram, Mail, Phone } from "lucide-react";

const navLinks = [
  { label: "Home", href: "#home" },
  { label: "Services", href: "#services" },
  { label: "Portfolio", href: "#portfolio" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

const socials = [
  {
    icon: Facebook,
    label: "Facebook",
    href: "https://www.facebook.com/IvanSorianoPhotography",
  },
  {
    icon: Instagram,
    label: "Instagram",
    href: "https://www.instagram.com/",
  },
  {
    icon: Mail,
    label: "Email",
    href: "mailto:ivp.photos@gmail.com",
  },
  {
    icon: Phone,
    label: "Phone",
    href: "tel:+639362886643",
  },
];

export function Footer() {
  const scrollTo = (href: string) => {
    document.querySelector(href)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <footer
      style={{
        backgroundColor: "var(--isp-bg-card)",
        borderTop: "1px solid rgba(200,169,110,0.12)",
      }}
      className="px-6 md:px-12 pt-20 pb-10"
    >
      <div className="max-w-7xl mx-auto">
        {/* Top row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 pb-14"
          style={{ borderBottom: "1px solid rgba(200,169,110,0.08)" }}
        >
          {/* Brand */}
          <div>
            <LogoFull height={44} className="mb-5" />
            <p
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--isp-text-muted)",
                fontSize: "14px",
                lineHeight: 1.8,
              }}
              className="max-w-xs"
            >
              Capturing life's most meaningful moments with artistry and heart.
              Based in Cavite, Philippines.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <p
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--isp-gold)",
                fontSize: "11px",
                letterSpacing: "0.25em",
              }}
              className="uppercase mb-5"
            >
              Navigation
            </p>
            <nav className="flex flex-col gap-3">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => scrollTo(link.href)}
                  style={{
                    fontFamily: "var(--font-body)",
                    color: "var(--isp-text-muted)",
                    fontSize: "14px",
                    textAlign: "left",
                  }}
                  className="hover:text-[var(--isp-cream)] transition-colors duration-200 w-fit"
                >
                  {link.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Contact */}
          <div>
            <p
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--isp-gold)",
                fontSize: "11px",
                letterSpacing: "0.25em",
              }}
              className="uppercase mb-5"
            >
              Get in Touch
            </p>
            <div className="space-y-3 mb-6">
              <a
                href="tel:+639362886643"
                style={{
                  fontFamily: "var(--font-body)",
                  color: "var(--isp-text-muted)",
                  fontSize: "14px",
                }}
                className="block hover:text-[var(--isp-cream)] transition-colors"
              >
                0936 288 6643
              </a>
              <a
                href="mailto:ivp.photos@gmail.com"
                style={{
                  fontFamily: "var(--font-body)",
                  color: "var(--isp-text-muted)",
                  fontSize: "14px",
                }}
                className="block hover:text-[var(--isp-cream)] transition-colors"
              >
                ivp.photos@gmail.com
              </a>
              <p
                style={{
                  fontFamily: "var(--font-body)",
                  color: "var(--isp-text-muted)",
                  fontSize: "14px",
                }}
              >
                Cavite, Philippines
              </p>
            </div>

            {/* Social icons */}
            <div className="flex gap-3">
              {socials.map((s) => {
                const Icon = s.icon;
                return (
                  <a
                    key={s.label}
                    href={s.href}
                    target={s.href.startsWith("http") ? "_blank" : undefined}
                    rel="noopener noreferrer"
                    aria-label={s.label}
                    style={{
                      backgroundColor: "rgba(31,72,48,0.25)",
                      border: "1px solid rgba(31,72,48,0.5)",
                      color: "var(--isp-text-muted)",
                    }}
                    className="w-9 h-9 flex items-center justify-center hover:bg-[var(--isp-green)] hover:border-[var(--isp-green)] hover:text-[var(--isp-cream)] transition-all duration-300"
                  >
                    <Icon size={14} />
                  </a>
                );
              })}
            </div>
          </div>
        </div>

        {/* Bottom row */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p
            style={{
              fontFamily: "var(--font-body)",
              color: "var(--isp-text-muted)",
              fontSize: "12px",
              letterSpacing: "0.05em",
            }}
          >
            © {new Date().getFullYear()} Ivan Soriano Photography. All rights reserved.
          </p>
          <p
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--isp-text-muted)",
              fontSize: "14px",
              fontStyle: "italic",
            }}
          >
            "Moments that matters."
          </p>
        </div>
      </div>
    </footer>
  );
}
