import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import PCResponseBox from '/src/components/PCResponseBox.vue';
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('PCResponseBox', PCResponseBox);
app.mount('#app')
