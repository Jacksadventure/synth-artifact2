/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./pages/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}', './app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        mainPurple: '#635FC7',
        lightPurple: '#A8A4FF',
        black: '#000112',
        veryDarkGray: '#20212C',
        darkGray: '#2B2C37',
        gray: '#3E3F4E',
        mediumGray: '#828FA3',
        lightGray: '#E4EBFA',
        veryLightGray: '#F4F7FD',
        red: '#EA5555',
        lightRed: '#FF9898',
      },
    },
  },
  plugins: [],
};
