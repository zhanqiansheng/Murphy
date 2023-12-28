import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // 'child_process': 'child_process-browser'
    }
  },
  // server: {
  //   proxy: {
  //       '/stop-processing': {
  //         target: 'https://region-31.seetacloud.com:20727/stop-processing',
  //         changeOrigin: true,
  //         // rewrite: (path) => path.replace(/^\/api/, '/stop-processing'),
  //     },
  //   },
  // },
})