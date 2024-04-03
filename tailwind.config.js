/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './BPLMM/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      backgroundImage: {
        'image': "url('/static/images/image.png')",
      }
    },
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
