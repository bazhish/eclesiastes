import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'static',
  site: 'https://bazhish.github.io',
  base: '/eclesiastes',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
