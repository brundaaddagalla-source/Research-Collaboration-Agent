/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0b1a3a",
          900: "#0f2147",
          800: "#15316b",
          700: "#1e3a8a",
          600: "#2648a3",
        },
        sky: {
          50: "#f3f7fd",
          100: "#e6f0fb",
          200: "#cfe3f7",
        },
        signal: {
          active: "#0f9d6d",
          underutilized: "#c98a1c",
          dormant: "#c23b3b",
        },
        crest: "#c0272d",
      },
      fontFamily: {
        display: ["Manrope", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      boxShadow: {
        panel: "0 1px 2px rgba(15, 33, 71, 0.06), 0 1px 12px rgba(15, 33, 71, 0.04)",
      },
    },
  },
  plugins: [],
};
