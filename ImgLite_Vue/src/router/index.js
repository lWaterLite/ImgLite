import { createRouter, createWebHistory} from "vue-router";
import Login from "@/view/authentication/Login.vue";
import Home from "@/view/Home.vue"
import Register from "@/view/authentication/Register.vue";
import Title from "@/view/image/Title.vue";
import Uploads from "@/view/image/main/Uploads.vue";
import View from "@/view/image/main/View.vue";

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
        path: '/title',
        component: Title,
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