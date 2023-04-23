/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/src/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#2272FF'
      },
    },
  },
  plugins: [],
}

