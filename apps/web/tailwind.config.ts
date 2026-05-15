import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#070b16',
        panel: 'rgba(17, 24, 39, 0.55)',
        accent: '#70f0ff',
        nebula: '#7c3aed',
        chrome: '#c7d2fe'
      },
      boxShadow: {
        glow: '0 0 40px rgba(112, 240, 255, 0.15)'
      },
      backgroundImage: {
        grid: 'linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px)'
      }
    }
  },
  plugins: []
};

export default config;
