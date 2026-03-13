/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "var(--ink)",
        accent: "var(--accent)",
        spice: "var(--accent-2)",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 20px 50px -28px rgba(15, 118, 110, 0.45)",
      },
    },
  },
  plugins: [],
};
