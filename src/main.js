import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'
import uuidGenerator from './services/uuidGenerator'

createApp(App)
.use(store)
.use(router)
.use(uuidGenerator)
.mount('#app')