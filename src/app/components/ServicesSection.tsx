import { motion } from "motion/react";
import { Heart, Star, CalendarDays } from "lucide-react";

const services = [
  {
    icon: Heart,
    title: "Weddings",
    subtitle: "Your Love Story, Beautifully Told",
    description:
      "From intimate ceremonies to grand celebrations, we capture every tear, every laugh, and every tender glance. Philippine heritage churches, garden venues, or destination weddings — we are there.",
    tags: ["Ceremony", "Reception", "Same Day Edit", "Pre-nuptial"],
  },
  {
    icon: Star,
    title: "Debuts & Cotillion",
    subtitle: "Celebrating Your 18th in Style",
    description:
      "Your debut is a milestone like no other. We craft editorial-quality imagery that captures the elegance, energy, and emotion of your grand entrance into womanhood.",
    tags: ["18 Roses & Candles", "Cotillion", "Same Day Edit", "Photo Booth"],
  },
  {
    icon: CalendarDays,
    title: "Events",
    subtitle: "Every Celebration Deserves Memories",
    description:
      "Gala nights, annual parties, corporate gatherings, and adult birthday celebrations — we bring the same premium standard to every event, big or small.",
    tags: ["Gala", "Annual Parties", "Corporate", "Birthdays"],
  },
];

function SectionLabel({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-4 mb-4">
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
        {text}
      </span>
    </div>
  );
}

export function ServicesSection() {
  return (
    <section
      id="services"
      style={{ backgroundColor: "var(--isp-bg)" }}
      className="py-28 px-6 md:px-12"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="mb-20"
        >
          <SectionLabel text="What We Offer" />
          <h2
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--isp-cream)",
              fontWeight: 300,
              lineHeight: 1.1,
            }}
            className="text-5xl md:text-6xl max-w-xl"
          >
            Stories worth
            <br />
            <em style={{ fontStyle: "italic", fontWeight: 400 }}>remembering.</em>
          </h2>
        </motion.div>

        {/* Service cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-px"
          style={{ backgroundColor: "rgba(200,169,110,0.1)" }}
        >
          {services.map((service, i) => {
            const Icon = service.icon;
            return (
              <motion.div
                key={service.title}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-60px" }}
                transition={{ duration: 0.7, delay: i * 0.15 }}
                style={{ backgroundColor: "var(--isp-bg-card)" }}
                className="group p-10 relative overflow-hidden cursor-default"
              >
                {/* Hover overlay */}
                <div
                  className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                  style={{
                    background:
                      "linear-gradient(135deg, rgba(31,72,48,0.15) 0%, transparent 70%)",
                  }}
                />

                {/* Top accent line */}
                <div
                  style={{ backgroundColor: "var(--isp-gold)", height: 1 }}
                  className="w-0 group-hover:w-full transition-all duration-500 mb-8"
                />
                <div
                  style={{ backgroundColor: "rgba(200,169,110,0.3)", height: 1 }}
                  className="absolute top-0 left-0 right-0 group-hover:opacity-0 transition-opacity duration-500"
                />

                <div className="relative z-10">
                  <div
                    style={{
                      backgroundColor: "rgba(31,72,48,0.4)",
                      border: "1px solid rgba(31,72,48,0.6)",
                    }}
                    className="w-12 h-12 flex items-center justify-center mb-6"
                  >
                    <Icon size={20} style={{ color: "var(--isp-gold)" }} />
                  </div>

                  <h3
                    style={{
                      fontFamily: "var(--font-display)",
                      color: "var(--isp-cream)",
                      fontWeight: 400,
                    }}
                    className="text-3xl mb-2"
                  >
                    {service.title}
                  </h3>

                  <p
                    style={{
                      fontFamily: "var(--font-body)",
                      color: "var(--isp-gold)",
                      letterSpacing: "0.05em",
                      fontSize: "12px",
                    }}
                    className="uppercase tracking-wide mb-5"
                  >
                    {service.subtitle}
                  </p>

                  <p
                    style={{
                      fontFamily: "var(--font-body)",
                      color: "var(--isp-text-muted)",
                      lineHeight: 1.8,
                      fontSize: "14px",
                    }}
                    className="mb-8"
                  >
                    {service.description}
                  </p>

                  <div className="flex flex-wrap gap-2">
                    {service.tags.map((tag) => (
                      <span
                        key={tag}
                        style={{
                          fontFamily: "var(--font-body)",
                          color: "var(--isp-text-muted)",
                          borderColor: "rgba(122,140,126,0.25)",
                          fontSize: "11px",
                          letterSpacing: "0.1em",
                        }}
                        className="border px-3 py-1 uppercase tracking-wider group-hover:border-[rgba(200,169,110,0.3)] group-hover:text-[var(--isp-cream)] transition-colors duration-300"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
