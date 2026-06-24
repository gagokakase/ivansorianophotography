import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Menu, X } from "lucide-react";
import { LogoFull } from "./LogoMark";

const navLinks = [
  { label: "Home", href: "#home" },
  { label: "Services", href: "#services" },
  { label: "Portfolio", href: "#portfolio" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const handleNavClick = (href: string) => {
    setMobileOpen(false);
    const el = document.querySelector(href);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      <motion.header
        initial={{ y: -80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        style={{
          backgroundColor: scrolled ? "rgba(8,12,9,0.92)" : "transparent",
          backdropFilter: scrolled ? "blur(16px)" : "none",
          borderBottom: scrolled ? "1px solid rgba(200,169,110,0.12)" : "1px solid transparent",
          transition: "background-color 0.4s ease, backdrop-filter 0.4s ease, border-color 0.4s ease",
        }}
        className="fixed top-0 left-0 right-0 z-50 px-6 md:px-12 py-4"
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <button onClick={() => handleNavClick("#home")} className="focus:outline-none">
            <LogoFull height={36} />
          </button>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <button
                key={link.href}
                onClick={() => handleNavClick(link.href)}
                style={{
                  fontFamily: "var(--font-body)",
                  color: "var(--isp-cream)",
                  letterSpacing: "0.1em",
                }}
                className="text-xs uppercase tracking-widest opacity-70 hover:opacity-100 transition-opacity duration-200"
              >
                {link.label}
              </button>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-4">
            <button
              onClick={() => handleNavClick("#contact")}
              style={{
                fontFamily: "var(--font-body)",
                borderColor: "var(--isp-gold)",
                color: "var(--isp-gold)",
                letterSpacing: "0.15em",
              }}
              className="text-xs uppercase tracking-widest px-6 py-2.5 border rounded-none hover:bg-[#C8A96E] hover:text-[#080C09] transition-all duration-300"
            >
              Book Now
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden"
            style={{ color: "var(--isp-cream)" }}
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </motion.header>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, x: "100%" }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: "100%" }}
            transition={{ duration: 0.35, ease: "easeInOut" }}
            style={{ backgroundColor: "var(--isp-bg-card)" }}
            className="fixed inset-0 z-40 flex flex-col items-center justify-center gap-8 md:hidden"
          >
            {navLinks.map((link) => (
              <button
                key={link.href}
                onClick={() => handleNavClick(link.href)}
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--isp-cream)",
                  letterSpacing: "0.08em",
                }}
                className="text-3xl font-light"
              >
                {link.label}
              </button>
            ))}
            <button
              onClick={() => handleNavClick("#contact")}
              style={{
                fontFamily: "var(--font-body)",
                borderColor: "var(--isp-gold)",
                color: "var(--isp-gold)",
                letterSpacing: "0.15em",
              }}
              className="text-sm uppercase tracking-widest px-8 py-3 border mt-4 hover:bg-[#C8A96E] hover:text-[#080C09] transition-all duration-300"
            >
              Book a Session
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
