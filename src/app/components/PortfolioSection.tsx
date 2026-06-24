import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
import { X, ZoomIn } from "lucide-react";
import img1 from "../../imports/image-1.png";
import img2 from "../../imports/image-2.png";
import img3 from "../../imports/image-3.png";
import img4 from "../../imports/image-4.png";

const photos = [
  {
    src: img1,
    alt: "Wedding at San Agustin Church, Intramuros",
    category: "Wedding",
    title: "Mark & Dianne",
    location: "Intramuros, Manila",
  },
  {
    src: img2,
    alt: "Portrait session — dramatic red lighting",
    category: "Portrait",
    title: "Leorah",
    location: "Studio",
  },
  {
    src: img3,
    alt: "Groom at the altar inside ornate church",
    category: "Wedding",
    title: "Mark & Dianne",
    location: "San Agustin Church",
  },
  {
    src: img4,
    alt: "Bride at the altar, joyful moment",
    category: "Wedding",
    title: "Mark & Dianne",
    location: "San Agustin Church",
  },
];

const categories = ["All", "Wedding", "Portrait"];

export function PortfolioSection() {
  const [activeCategory, setActiveCategory] = useState("All");
  const [lightbox, setLightbox] = useState<(typeof photos)[0] | null>(null);

  const filtered =
    activeCategory === "All"
      ? photos
      : photos.filter((p) => p.category === activeCategory);

  return (
    <section
      id="portfolio"
      style={{ backgroundColor: "var(--isp-bg-section)" }}
      className="py-28 px-6 md:px-12"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7 }}
          className="flex flex-col md:flex-row md:items-end justify-between mb-14 gap-8"
        >
          <div>
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
                Portfolio
              </span>
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
              The Work
            </h2>
          </div>

          {/* Filter tabs */}
          <div className="flex gap-1">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                style={{
                  fontFamily: "var(--font-body)",
                  letterSpacing: "0.15em",
                  fontSize: "11px",
                  color:
                    activeCategory === cat ? "var(--isp-bg)" : "var(--isp-text-muted)",
                  backgroundColor:
                    activeCategory === cat ? "var(--isp-gold)" : "transparent",
                  borderColor:
                    activeCategory === cat
                      ? "var(--isp-gold)"
                      : "rgba(122,140,126,0.3)",
                }}
                className="border px-5 py-2 uppercase tracking-wider transition-all duration-300 hover:border-[var(--isp-gold)] hover:text-[var(--isp-cream)]"
              >
                {cat}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Masonry grid */}
        <motion.div
          layout
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <ResponsiveMasonry
            columnsCountBreakPoints={{ 350: 1, 640: 2, 1024: 3 }}
          >
            <Masonry gutter="12px">
              {filtered.map((photo, i) => (
                <motion.div
                  key={photo.src}
                  layout
                  initial={{ opacity: 0, scale: 0.97 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.97 }}
                  transition={{ duration: 0.5, delay: i * 0.08 }}
                  className="relative group cursor-pointer overflow-hidden"
                  onClick={() => setLightbox(photo)}
                >
                  <img
                    src={photo.src}
                    alt={photo.alt}
                    className="w-full block transition-transform duration-700 group-hover:scale-105"
                    style={{ display: "block" }}
                  />
                  {/* Hover overlay */}
                  <div
                    className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-400 flex flex-col justify-end p-6"
                    style={{
                      background:
                        "linear-gradient(to top, rgba(8,12,9,0.88) 0%, rgba(8,12,9,0.3) 50%, transparent 100%)",
                    }}
                  >
                    <div className="flex items-end justify-between">
                      <div>
                        <p
                          style={{
                            fontFamily: "var(--font-body)",
                            color: "var(--isp-gold)",
                            fontSize: "10px",
                            letterSpacing: "0.2em",
                          }}
                          className="uppercase mb-1"
                        >
                          {photo.category}
                        </p>
                        <p
                          style={{
                            fontFamily: "var(--font-display)",
                            color: "var(--isp-cream)",
                            fontSize: "20px",
                            fontWeight: 400,
                          }}
                        >
                          {photo.title}
                        </p>
                        <p
                          style={{
                            fontFamily: "var(--font-body)",
                            color: "rgba(242,237,228,0.6)",
                            fontSize: "12px",
                          }}
                        >
                          {photo.location}
                        </p>
                      </div>
                      <div
                        style={{
                          border: "1px solid rgba(200,169,110,0.5)",
                          color: "var(--isp-gold)",
                        }}
                        className="w-9 h-9 flex items-center justify-center flex-shrink-0"
                      >
                        <ZoomIn size={14} />
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </Masonry>
          </ResponsiveMasonry>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-14 flex justify-center"
        >
          <a
            href="https://www.facebook.com/IvanSorianoPhotography"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontFamily: "var(--font-body)",
              color: "var(--isp-cream)",
              borderColor: "rgba(242,237,228,0.2)",
              letterSpacing: "0.2em",
              fontSize: "12px",
            }}
            className="border px-10 py-4 uppercase tracking-widest hover:border-[var(--isp-gold)] hover:text-[var(--isp-gold)] transition-all duration-300"
          >
            View Full Gallery on Facebook
          </a>
        </motion.div>
      </div>

      {/* Lightbox */}
      <AnimatePresence>
        {lightbox && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-10"
            style={{ backgroundColor: "rgba(8,12,9,0.95)" }}
            onClick={() => setLightbox(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ duration: 0.35 }}
              className="relative max-w-4xl w-full max-h-[85vh] flex items-center justify-center"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={lightbox.src}
                alt={lightbox.alt}
                className="max-w-full max-h-[80vh] object-contain"
              />
              <button
                onClick={() => setLightbox(null)}
                style={{
                  backgroundColor: "rgba(8,12,9,0.8)",
                  border: "1px solid rgba(200,169,110,0.3)",
                  color: "var(--isp-cream)",
                }}
                className="absolute top-3 right-3 w-10 h-10 flex items-center justify-center hover:border-[var(--isp-gold)] transition-colors"
              >
                <X size={16} />
              </button>
              <div className="absolute bottom-3 left-0 right-0 text-center">
                <p
                  style={{
                    fontFamily: "var(--font-display)",
                    color: "var(--isp-cream)",
                    fontSize: "18px",
                  }}
                >
                  {lightbox.title}
                </p>
                <p
                  style={{
                    fontFamily: "var(--font-body)",
                    color: "var(--isp-gold)",
                    fontSize: "12px",
                    letterSpacing: "0.15em",
                  }}
                  className="uppercase"
                >
                  {lightbox.location}
                </p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
