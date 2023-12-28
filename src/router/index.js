import { createRouter, createWebHistory } from 'vue-router'
import Murphy from '/src/views/murphy.vue'
import Main from '/src/views/main.vue'
import Shop from '/src/views/shop.vue'
import About from '/src/views/about.vue'
import Contact from '/src/views/contact.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', redirect: '/main'},
    {
      path: '/murphy', component: Murphy,
      children: [
        {path: '/main', component: Main, meta: { title: '超思维智能 - 首页' }},
        {path: '/shop', component: Shop, meta: { title: '超思维智能 - 商城' }},
        {path: '/about', component: About, meta: { title: '超思维智能 - 关于' }},
        {path: '/contact', component: Contact, meta: { title: '超思维智能 - 联系我们' }},
      ]
    }
  ]
})

export default router
