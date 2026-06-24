interface LogoMarkProps {
  size?: number;
  className?: string;
}

export function LogoMark({ size = 40, className = "" }: LogoMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Top-left quadrant: white fill with bottom-right arc cut */}
      <path
        d="M10 10 H50 Q50 50 10 50 Z"
        fill="white"
      />
      {/* Top-right quadrant: green fill with bottom-left arc cut */}
      <path
        d="M50 10 H90 V50 Q50 50 50 10 Z"
        fill="#1F4830"
      />
      {/* Bottom-left quadrant: green fill with top-right arc cut */}
      <path
        d="M10 50 Q50 50 50 90 H10 Z"
        fill="#1F4830"
      />
      {/* Bottom-right quadrant: white fill with top-left arc cut */}
      <path
        d="M50 50 Q50 90 90 90 V50 Z"
        fill="white"
      />
    </svg>
  );
}

export function LogoFull({ height = 48, className = "" }: { height?: number; className?: string }) {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <LogoMark size={height} />
      <div className="flex flex-col leading-none">
        <span
          style={{
            fontFamily: "var(--font-display)",
            letterSpacing: "0.12em",
            color: "var(--isp-cream)",
          }}
          className="text-sm font-medium tracking-widest uppercase"
        >
          Ivan Soriano
        </span>
        <span
          style={{
            fontFamily: "var(--font-display)",
            letterSpacing: "0.2em",
            color: "var(--isp-text-muted)",
          }}
          className="text-xs tracking-widest uppercase"
        >
          Photography
        </span>
      </div>
    </div>
  );
}
