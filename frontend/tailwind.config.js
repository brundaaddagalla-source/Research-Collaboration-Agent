/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],

  theme: {
    extend: {
      colors: {
        navy: {
          950: "#0c1f3a",
          900: "#12315a",
          800: "#17365d",
          700: "#1c4a80",
          600: "#1677d2",
        },

        sky: {
          50: "#f6f9fe",
          100: "#eef6ff",
          200: "#dceafa",
        },

        signal: {
          active: "#23835e",
          underutilized: "#bd7622",
          dormant: "#c65050",
        },

        accent: {
          blue: "#1677d2",
          teal: "#2f8bea",
          green: "#2b9b6b",
          purple: "#7759cf",
          pink: "#e0507a",
          orange: "#d68b32",
          gold: "#d4a017",
        },

        crest: "#c0272d",

        surface: {
          ink: "#20344d",
          muted: "#718198",
          line: "#e3ebf5",
          panel: "#ffffff",
        },
      },

      backgroundImage: {
        hero:
          "linear-gradient(120deg, #eef6ff 0%, #e4f0ff 58%, #f9fbff 100%)",
      },

      fontFamily: {
        display: ["Manrope", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },

      boxShadow: {
        panel: "0 8px 28px rgba(36, 82, 126, 0.07)",
      },

      borderRadius: {
        panel: "14px",
      },
    },
  },

  plugins: [],
};

