/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './BPLMM/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      backgroundImage: {
        'logo': "url('/static/images/philhealth-logo.png')",
        
      },

      backgroundColor: {
        'sideBarBgColor': '#4aca1c'
      }
    },
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
