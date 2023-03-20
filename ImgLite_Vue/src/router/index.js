import { createRouter, createWebHistory} from "vue-router";
import Login from "@/view/gateway/Login.vue";
import Home from "@/view/Home.vue"
import Register from "@/view/gateway/Register.vue";
import BedRock from "@/view/bedrock/BedRock.vue";
import Uploads from "@/view/bedrock/main/Uploads.vue";
import View from "@/view/bedrock/main/View.vue";

const routes = [
    {
        path: '/',
        redirect: '/home'
    },
    {
        path: '/home',
        component: Home
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/bedrock',
        component: BedRock,
        children: [{
            path: '/uploads',
            component: Uploads
        }, {
            path: '/view',
            component: View
        }],
        redirect: '/view'
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router