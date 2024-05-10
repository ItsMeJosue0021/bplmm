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
        'logo': "url('/static/images/images_Philhealth_Logo.png')",
        'loginBg': "url('/static/images/images_Philhealth_Logo.png')",
        'bgImage': "url('/static/images/philhealth-bg.png')",
        'miniBg' : "url('/static/images/miniBG.jpg')",
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
      'primary': '#43B02A',
    }
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
