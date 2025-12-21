import { createApp } from 'vue'
import App from './App.vue'
import router from './router' 
const app = createApp(App)

app.use(router) // 2. Vue 앱에 라우터를 등록

app.mount('#app')