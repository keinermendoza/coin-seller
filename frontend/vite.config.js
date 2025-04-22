import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: path.join(path.dirname(__dirname), "project", "assets"),
    rollupOptions: {
      input: {
        main: path.resolve('./src/main.jsx'),
      }
    }
  }
})
