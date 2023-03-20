import { createApp } from 'vue'
import App from './App.vue'
import router from "./router/index";
import './style.css'

import axios from "axios";
import VueAxios from "vue-axios";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueCookies from "vue-cookies"
import VueClipboards from "vue-clipboard2";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
app.use(ElementPlus)
app.use(VueAxios, axios)
app.use(VueCookies)
app.use(VueClipboards)
app.mount('#app')
export {app}
