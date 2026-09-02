/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      colors: {
        'signal-teal': '#00d2d3',
        'threat-red': '#ff5252',
        'threat-amber': '#ffda79',
      }
    },
  },
  plugins: [],
}
