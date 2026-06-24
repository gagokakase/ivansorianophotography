import { motion } from "motion/react";
import { Quote } from "lucide-react";

const testimonials = [
  {
    name: "Mark & Dianne",
    event: "Wedding · San Agustin Church, Intramuros",
    quote:
      "Ivan captured our wedding day with such artistry and grace. Every photo tells the story of our love — from the nerves before the ceremony to the pure joy at the reception. We will treasure these memories forever.",
    initial: "M",
  },
  {
    name: "Leorah C.",
    event: "Debut · Same Day Edit",
    quote:
      "I was blown away by how quickly he turned around our same day edit. The cinematic quality, the angles, the lighting — it was everything I dreamed my debut would look like. He made me feel like a star.",
    initial: "L",
  },
  {
    name: "The Santos Family",
    event: "Annual Gala · Cavite",
    quote:
      "We have booked Ivan for our company's annual gala for three years running. His team is professional, discreet, and always delivers stunning results. The photos elevate the entire event every single time.",
    initial: "S",
  },
];

export function TestimonialsSection() {
  return (
    <section
      style={{
        backgroundColor: "var(--isp-bg-card)",
        borderTop: "1px solid rgba(200,169,110,0.08)",
        borderBottom: "1px solid rgba(200,169,110,0.08)",
      }}
      className="py-28 px-6 md:px-12 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-4 mb-4">
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
              Kind Words
            </span>
            <div style={{ width: 32, height: 1, backgroundColor: "var(--isp-gold)" }} />
          </div>
          <h2
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--isp-cream)",
              fontWeight: 300,
              lineHeight: 1.1,
            }}
            className="text-5xl md:text-6xl"
          >
            What clients say
          </h2>
        </motion.div>

        {/* Testimonial cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.name}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.7, delay: i * 0.15 }}
              style={{
                backgroundColor: "var(--isp-bg)",
                border: "1px solid rgba(200,169,110,0.1)",
              }}
              className="p-8 flex flex-col group hover:border-[rgba(200,169,110,0.3)] transition-colors duration-400"
            >
              <Quote
                size={24}
                style={{ color: "var(--isp-gold)", opacity: 0.5 }}
                className="mb-6 flex-shrink-0"
              />

              <p
                style={{
                  fontFamily: "var(--font-display)",
                  color: "var(--isp-cream)",
                  fontSize: "19px",
                  lineHeight: 1.7,
                  fontWeight: 300,
                  fontStyle: "italic",
                }}
                className="flex-1 mb-8"
              >
                "{t.quote}"
              </p>

              <div
                style={{ borderTop: "1px solid rgba(200,169,110,0.15)" }}
                className="pt-6 flex items-center gap-4"
              >
                <div
                  style={{
                    backgroundColor: "var(--isp-green)",
                    border: "1px solid var(--isp-green-light)",
                    color: "var(--isp-cream)",
                    fontFamily: "var(--font-display)",
                    fontSize: "18px",
                  }}
                  className="w-10 h-10 flex items-center justify-center flex-shrink-0"
                >
                  {t.initial}
                </div>
                <div>
                  <p
                    style={{
                      fontFamily: "var(--font-body)",
                      color: "var(--isp-cream)",
                      fontSize: "14px",
                      fontWeight: 500,
                    }}
                  >
                    {t.name}
                  </p>
                  <p
                    style={{
                      fontFamily: "var(--font-body)",
                      color: "var(--isp-text-muted)",
                      fontSize: "12px",
                    }}
                  >
                    {t.event}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
