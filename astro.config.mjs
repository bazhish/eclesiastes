import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'static',
  site: process.env.GITHUB_ACTIONS ? 'https://bazhish.github.io' : undefined,
  base: process.env.GITHUB_ACTIONS ? '/gabarito-3b' : '/',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
