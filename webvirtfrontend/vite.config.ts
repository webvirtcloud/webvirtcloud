import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => {
  const isDevelopment = mode === 'development';

  return {
    optimizeDeps: {
      esbuildOptions: {
        target: 'es2020',
      },
    },
    plugins: [
      react({
        babel: { plugins: ['babel-plugin-macros', 'babel-plugin-styled-components'] },
      }),
    ],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    css: {
      modules: {
        generateScopedName: isDevelopment
          ? '[name]__[local]__[hash:base64:5]'
          : '[hash:base64:5]',
      },
    },
  };
});
