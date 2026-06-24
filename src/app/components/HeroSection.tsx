import { motion } from "motion/react";
import { ChevronDown } from "lucide-react";
import heroImg from "../../imports/image-1.png";

export function HeroSection() {
  const scrollToNext = () => {
    const el = document.querySelector("#services");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section
      id="home"
      className="relative w-full h-screen min-h-[600px] flex items-center justify-center overflow-hidden"
    >
      {/* Background image */}
      <div className="absolute inset-0">
        <img
          src={heroImg}
          alt="Ivan Soriano Photography — Wedding at San Agustin Church"
          className="w-full h-full object-cover object-center"
          style={{ transform: "scale(1.05)" }}
        />
        {/* Multi-layer gradient overlay for premium dark mood */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to bottom, rgba(8,12,9,0.55) 0%, rgba(8,12,9,0.2) 40%, rgba(8,12,9,0.75) 100%)",
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to right, rgba(8,12,9,0.5) 0%, transparent 60%)",
          }}
        />
      </div>

      {/* Grain texture overlay */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
          backgroundRepeat: "repeat",
          backgroundSize: "128px",
        }}
      />

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 md:px-12 w-full flex flex-col justify-end pb-28 h-full">
        {/* Gold accent line */}
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: 64 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          style={{ backgroundColor: "var(--isp-gold)", height: 1 }}
          className="mb-6"
        />

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          style={{
            fontFamily: "var(--font-body)",
            color: "var(--isp-gold)",
            letterSpacing: "0.3em",
          }}
          className="text-xs uppercase tracking-widest mb-4"
        >
          Cavite, Philippines
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.5, ease: "easeOut" }}
          style={{
            fontFamily: "var(--font-display)",
            color: "var(--isp-cream)",
            lineHeight: 1.05,
            fontWeight: 300,
          }}
          className="text-6xl md:text-8xl lg:text-9xl mb-4 max-w-4xl"
        >
          Moments
          <br />
          <em style={{ fontStyle: "italic", fontWeight: 400 }}>that matters.</em>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          style={{
            fontFamily: "var(--font-body)",
            color: "rgba(242,237,228,0.65)",
            letterSpacing: "0.05em",
          }}
          className="text-sm md:text-base mb-10 max-w-md"
        >
          Wedding · Debut · Events · Portrait Photography
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="flex flex-col sm:flex-row gap-4"
        >
          <button
            onClick={() => {
              document.querySelector("#portfolio")?.scrollIntoView({ behavior: "smooth" });
            }}
            style={{
              backgroundColor: "var(--isp-green)",
              color: "var(--isp-cream)",
              fontFamily: "var(--font-body)",
              letterSpacing: "0.2em",
              border: "1px solid var(--isp-green-light)",
            }}
            className="text-xs uppercase tracking-widest px-8 py-4 hover:bg-[#2D5A3D] transition-all duration-300"
          >
            View Portfolio
          </button>
          <button
            onClick={() => {
              document.querySelector("#contact")?.scrollIntoView({ behavior: "smooth" });
            }}
            style={{
              color: "var(--isp-cream)",
              fontFamily: "var(--font-body)",
              letterSpacing: "0.2em",
              border: "1px solid rgba(242,237,228,0.3)",
            }}
            className="text-xs uppercase tracking-widest px-8 py-4 hover:border-[var(--isp-gold)] hover:text-[var(--isp-gold)] transition-all duration-300"
          >
            Book a Session
          </button>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.button
        onClick={scrollToNext}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 1.4 }}
        style={{ color: "var(--isp-cream)" }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-50 hover:opacity-100 transition-opacity"
      >
        <span
          style={{ fontFamily: "var(--font-body)", letterSpacing: "0.2em", fontSize: "10px" }}
          className="uppercase tracking-widest"
        >
          Scroll
        </span>
        <motion.div
          animate={{ y: [0, 6, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        >
          <ChevronDown size={16} />
        </motion.div>
      </motion.button>
    </section>
  );
}
