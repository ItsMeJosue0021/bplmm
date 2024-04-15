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
      },

      width:{
        '85': '85%'
      },

      zIndex: {
        '100': '100',
      }
    },

    colors: {
      'themeColor': '#156913',
    }
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
