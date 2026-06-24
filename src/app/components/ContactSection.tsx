import { useForm } from "react-hook-form";
import { motion } from "motion/react";
import { toast } from "sonner";
import { Phone, Mail, MapPin, Facebook } from "lucide-react";

interface BookingForm {
  name: string;
  email: string;
  phone: string;
  eventType: string;
  eventDate: string;
  message: string;
}

const contactDetails = [
  {
    icon: Phone,
    label: "Phone",
    value: "0936 288 6643",
    href: "tel:+639362886643",
  },
  {
    icon: Mail,
    label: "Email",
    value: "ivp.photos@gmail.com",
    href: "mailto:ivp.photos@gmail.com",
  },
  {
    icon: MapPin,
    label: "Location",
    value: "Cavite, Philippines",
    href: null,
  },
  {
    icon: Facebook,
    label: "Facebook",
    value: "Ivan Soriano Photography",
    href: "https://www.facebook.com/IvanSorianoPhotography",
  },
];

const inputStyle: React.CSSProperties = {
  backgroundColor: "transparent",
  borderBottom: "1px solid rgba(122,140,126,0.35)",
  borderTop: "none",
  borderLeft: "none",
  borderRight: "none",
  color: "var(--isp-cream)",
  fontFamily: "var(--font-body)",
  fontSize: "14px",
  outline: "none",
  width: "100%",
  padding: "12px 0",
  transition: "border-color 0.3s",
};

const labelStyle: React.CSSProperties = {
  fontFamily: "var(--font-body)",
  color: "var(--isp-text-muted)",
  fontSize: "11px",
  letterSpacing: "0.2em",
  textTransform: "uppercase",
  display: "block",
  marginBottom: "4px",
};

export function ContactSection() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<BookingForm>();

  const onSubmit = async (data: BookingForm) => {
    await new Promise((r) => setTimeout(r, 800));
    console.log("Booking inquiry:", data);
    toast.success("Message sent! Ivan will be in touch soon.", {
      style: {
        backgroundColor: "var(--isp-bg-card)",
        border: "1px solid rgba(200,169,110,0.3)",
        color: "var(--isp-cream)",
      },
    });
    reset();
  };

  return (
    <section
      id="contact"
      style={{ backgroundColor: "var(--isp-bg)" }}
      className="py-28 px-6 md:px-12"
    >
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-28">
          {/* Left: info */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.8 }}
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
                Book a Session
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
              Let's create
              <br />
              <em style={{ fontStyle: "italic", fontWeight: 400 }}>something beautiful.</em>
            </h2>

            <p
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--isp-text-muted)",
                fontSize: "15px",
                lineHeight: 1.9,
              }}
              className="mb-12"
            >
              Ready to book Ivan for your wedding, debut, or event? Fill out the form and we'll get back to you with availability and packages. We love hearing about your vision.
            </p>

            {/* Contact details */}
            <div className="space-y-6">
              {contactDetails.map((item) => {
                const Icon = item.icon;
                const content = (
                  <div className="flex items-start gap-4 group">
                    <div
                      style={{
                        backgroundColor: "rgba(31,72,48,0.3)",
                        border: "1px solid rgba(31,72,48,0.5)",
                        color: "var(--isp-gold)",
                      }}
                      className="w-10 h-10 flex items-center justify-center flex-shrink-0 mt-0.5 group-hover:bg-[rgba(31,72,48,0.6)] transition-colors"
                    >
                      <Icon size={16} />
                    </div>
                    <div>
                      <p
                        style={{
                          fontFamily: "var(--font-body)",
                          color: "var(--isp-text-muted)",
                          fontSize: "11px",
                          letterSpacing: "0.15em",
                        }}
                        className="uppercase mb-0.5"
                      >
                        {item.label}
                      </p>
                      <p
                        style={{
                          fontFamily: "var(--font-body)",
                          color: "var(--isp-cream)",
                          fontSize: "15px",
                        }}
                      >
                        {item.value}
                      </p>
                    </div>
                  </div>
                );

                return item.href ? (
                  <a key={item.label} href={item.href} target={item.href.startsWith("http") ? "_blank" : undefined} rel="noopener noreferrer" className="block hover:opacity-80 transition-opacity">
                    {content}
                  </a>
                ) : (
                  <div key={item.label}>{content}</div>
                );
              })}
            </div>
          </motion.div>

          {/* Right: form */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                <div>
                  <label style={labelStyle}>Full Name</label>
                  <input
                    {...register("name", { required: true })}
                    placeholder="Your full name"
                    style={{
                      ...inputStyle,
                      borderBottomColor: errors.name
                        ? "rgba(212,24,61,0.7)"
                        : "rgba(122,140,126,0.35)",
                    }}
                    onFocus={(e) =>
                      (e.target.style.borderBottomColor = "var(--isp-gold)")
                    }
                    onBlur={(e) =>
                      (e.target.style.borderBottomColor = errors.name
                        ? "rgba(212,24,61,0.7)"
                        : "rgba(122,140,126,0.35)")
                    }
                  />
                </div>
                <div>
                  <label style={labelStyle}>Email</label>
                  <input
                    {...register("email", { required: true, pattern: /^\S+@\S+$/i })}
                    placeholder="your@email.com"
                    type="email"
                    style={{
                      ...inputStyle,
                      borderBottomColor: errors.email
                        ? "rgba(212,24,61,0.7)"
                        : "rgba(122,140,126,0.35)",
                    }}
                    onFocus={(e) =>
                      (e.target.style.borderBottomColor = "var(--isp-gold)")
                    }
                    onBlur={(e) =>
                      (e.target.style.borderBottomColor = errors.email
                        ? "rgba(212,24,61,0.7)"
                        : "rgba(122,140,126,0.35)")
                    }
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                <div>
                  <label style={labelStyle}>Phone</label>
                  <input
                    {...register("phone")}
                    placeholder="09XX XXX XXXX"
                    type="tel"
                    style={inputStyle}
                    onFocus={(e) =>
                      (e.target.style.borderBottomColor = "var(--isp-gold)")
                    }
                    onBlur={(e) =>
                      (e.target.style.borderBottomColor = "rgba(122,140,126,0.35)")
                    }
                  />
                </div>
                <div>
                  <label style={labelStyle}>Event Type</label>
                  <select
                    {...register("eventType", { required: true })}
                    style={{
                      ...inputStyle,
                      backgroundColor: "var(--isp-bg)",
                      cursor: "pointer",
                    }}
                  >
                    <option value="" style={{ backgroundColor: "var(--isp-bg)" }}>
                      Select event type
                    </option>
                    <option value="wedding" style={{ backgroundColor: "var(--isp-bg)" }}>
                      Wedding
                    </option>
                    <option value="debut" style={{ backgroundColor: "var(--isp-bg)" }}>
                      Debut & Cotillion
                    </option>
                    <option value="events" style={{ backgroundColor: "var(--isp-bg)" }}>
                      Events / Gala / Parties
                    </option>
                    <option value="portrait" style={{ backgroundColor: "var(--isp-bg)" }}>
                      Portrait
                    </option>
                  </select>
                </div>
              </div>

              <div>
                <label style={labelStyle}>Event Date</label>
                <input
                  {...register("eventDate")}
                  type="date"
                  style={{
                    ...inputStyle,
                    colorScheme: "dark",
                  }}
                  onFocus={(e) =>
                    (e.target.style.borderBottomColor = "var(--isp-gold)")
                  }
                  onBlur={(e) =>
                    (e.target.style.borderBottomColor = "rgba(122,140,126,0.35)")
                  }
                />
              </div>

              <div>
                <label style={labelStyle}>Message</label>
                <textarea
                  {...register("message", { required: true })}
                  placeholder="Tell us about your event, venue, vision..."
                  rows={4}
                  style={{
                    ...inputStyle,
                    resize: "none",
                    borderBottom: "1px solid rgba(122,140,126,0.35)",
                    borderBottomColor: errors.message
                      ? "rgba(212,24,61,0.7)"
                      : "rgba(122,140,126,0.35)",
                  }}
                  onFocus={(e) =>
                    (e.target.style.borderBottomColor = "var(--isp-gold)")
                  }
                  onBlur={(e) =>
                    (e.target.style.borderBottomColor = errors.message
                      ? "rgba(212,24,61,0.7)"
                      : "rgba(122,140,126,0.35)")
                  }
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                style={{
                  backgroundColor: isSubmitting ? "var(--isp-green-dark)" : "var(--isp-green)",
                  color: "var(--isp-cream)",
                  fontFamily: "var(--font-body)",
                  letterSpacing: "0.2em",
                  fontSize: "12px",
                  border: "1px solid var(--isp-green-light)",
                  cursor: isSubmitting ? "not-allowed" : "pointer",
                  transition: "all 0.3s",
                  width: "100%",
                  padding: "16px 32px",
                }}
                className="uppercase tracking-widest hover:bg-[var(--isp-green-light)] disabled:opacity-60"
              >
                {isSubmitting ? "Sending..." : "Send Inquiry"}
              </button>
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
