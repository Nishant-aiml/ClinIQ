import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

/**
 * Vite configuration for ClinIQ
 * Sets up React plugin and path aliases for clean imports.
 */
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3056,
    strictPort: true,
    host: true,
    allowedHosts: ['charging-lend-scoff.ngrok-free.dev', '.ngrok-free.app', '.ngrok.io', 'all'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8056',
        changeOrigin: true,
        secure: false,
      },
      '/docs': {
        target: 'http://127.0.0.1:8056',
        changeOrigin: true,
        secure: false,
      },
      '/openapi.json': {
        target: 'http://127.0.0.1:8056',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
