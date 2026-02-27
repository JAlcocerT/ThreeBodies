/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'void': '#05070A',
        'pulsar': '#00F0FF',
        'event-horizon': '#1A0B2E',
        'paper': '#E8E4DD',
        'supernova': '#FFFFFF',
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      backgroundImage: {
        'radial-at-b': 'radial-gradient(circle at bottom, var(--tw-gradient-stops))',
      }
    },
  },
  plugins: [],
}
