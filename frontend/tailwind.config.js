/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#10231f',
        leaf: '#1f6f5b',
        mint: '#dff5e8',
        ember: '#d9532f',
        gold: '#f2b84b',
        paper: '#fbfaf6',
      },
      boxShadow: {
        soft: '0 16px 45px rgba(16, 35, 31, 0.12)',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
