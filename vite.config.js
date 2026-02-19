import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    fs: {
      allow: ['..']
    },
    watch: {
      ignored: ['**/memory/**', '**/simulation/**']
    }
  }
})


