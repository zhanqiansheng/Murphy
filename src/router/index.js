import { createRouter, createWebHistory } from 'vue-router'
import Main from '/src/views/main.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', redirect: '/main'},
    {path: '/main', component: Main}
  ]
})

export default router
