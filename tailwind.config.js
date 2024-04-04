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
        'logo': "url('/static/images/philhealth-logo.png')",
        'loginBg': "url('/static/images/philhealth-login.png')",
      }
    },
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
