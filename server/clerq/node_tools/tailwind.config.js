/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../**/templates/**/*.{html,js}",
    "../**/forms.py"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["autumn"]
  }
}

