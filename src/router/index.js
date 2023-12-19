import { createRouter, createWebHistory } from 'vue-router'
import Murphy from '/src/views/murphy.vue'
import Main from '/src/views/main.vue'
import Shop from '/src/views/shop.vue'
import About from '/src/views/about.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', redirect: '/main'},
    {
      path: '/murphy', component: Murphy,
      children: [
        {path: '/main', component: Main},
        {path: '/shop', component: Shop},
        {path: '/about', component: About},
      ]
    }
  ]
})

export default router
