import { motion } from "motion/react";
import { LogoMark } from "./LogoMark";
import portraitImg from "../../imports/image-3.png";

const stats = [
  { number: "500+", label: "Events Captured" },
  { number: "8+", label: "Years of Experience" },
  { number: "100%", label: "Client Satisfaction" },
];

export function AboutSection() {
  return (
    <section
      id="about"
      style={{ backgroundColor: "var(--isp-bg)" }}
      className="py-28 px-6 md:px-12 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24 items-center">
          {/* Image column */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.9, ease: "easeOut" }}
            className="relative"
          >
            {/* Background accent box */}
            <div
              style={{
                backgroundColor: "var(--isp-green)",
                opacity: 0.25,
              }}
              className="absolute -left-4 -top-4 w-48 h-64 -z-10"
            />

            <div className="relative overflow-hidden">
              <img
                src={portraitImg}
                alt="Ivan Soriano — Photographer"
                className="w-full object-cover"
                style={{ maxHeight: "620px", objectPosition: "top" }}
              />
              {/* Bottom gradient */}
              <div
                className="absolute bottom-0 left-0 right-0 h-32"
                style={{
                  background:
                    "linear-gradient(to top, var(--isp-bg) 0%, transparent 100%)",
                }}
              />
            </div>

            {/* Floating stat card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.4 }}
              style={{
                backgroundColor: "var(--isp-bg-card)",
                border: "1px solid rgba(200,169,110,0.2)",
              }}
              className="absolute -bottom-6 -right-4 md:-right-8 p-6 flex items-center gap-5"
            >
              <LogoMark size={48} />
              <div>
                <p
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--isp-cream)",
                    fontSize: "28px",
                    fontWeight: 400,
                    lineHeight: 1,
                  }}
                >
                  Ivan Soriano
                </p>
                <p
                  style={{
                    fontFamily: "var(--font-body)",
                    color: "var(--isp-gold)",
                    fontSize: "11px",
                    letterSpacing: "0.2em",
                  }}
                  className="uppercase"
                >
                  Lead Photographer
                </p>
              </div>
            </motion.div>
          </motion.div>

          {/* Text column */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.9, ease: "easeOut", delay: 0.1 }}
          >
            <div className="flex items-center gap-4 mb-6">
              <div style={{ width: 32, height: 1, backgroundColor: "var(--isp-gold)" }} />
              <span
                style={{
                  fontFamily: "var(--font-body)",
                  color: "var(--isp-gold)",
                  letterSpacing: "0.3em",
                  fontSize: "11px",
                }}
                className="uppercase"
              >
                About
              </span>
            </div>

            <h2
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--isp-cream)",
                fontWeight: 300,
                lineHeight: 1.1,
              }}
              className="text-5xl md:text-6xl mb-8"
            >
              Behind the
              <br />
              <em style={{ fontStyle: "italic", fontWeight: 400 }}>lens.</em>
            </h2>

            <div
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--isp-text-muted)",
                lineHeight: 1.9,
                fontSize: "15px",
              }}
              className="space-y-4 mb-10"
            >
              <p>
                Based in Cavite, Philippines, Ivan Soriano Photography was born out of a deep passion
                for storytelling through imagery. Every click of the shutter is an act of preservation —
                freezing a feeling, a glance, a heartbeat in time.
              </p>
              <p>
                Specializing in weddings, debut celebrations, and events, we bring a cinematic,
                editorial eye to every occasion. Our approach is quiet, unobtrusive, and deeply human
                — we let moments unfold naturally, and we are there to capture them.
              </p>
              <p>
                From the grandeur of heritage churches in Intramuros to intimate garden ceremonies
                across Cavite, we have had the privilege of telling some of the most beautiful stories
                in the Philippines.
              </p>
            </div>

            {/* Stats */}
            <div
              style={{ borderTop: "1px solid rgba(200,169,110,0.15)" }}
              className="grid grid-cols-3 pt-8 gap-6"
            >
              {stats.map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: 0.5 + i * 0.1 }}
                >
                  <p
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--isp-cream)",
                      fontSize: "36px",
                      fontWeight: 300,
                      lineHeight: 1,
                    }}
                    className="mb-1"
                  >
                    {stat.number}
                  </p>
                  <p
                    style={{
                      fontFamily: "var(--font-body)",
                      color: "var(--isp-text-muted)",
                      fontSize: "12px",
                      letterSpacing: "0.05em",
                    }}
                  >
                    {stat.label}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
