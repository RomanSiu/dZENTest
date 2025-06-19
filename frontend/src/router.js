import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import CommentPage from './components/CommentPage.vue'
import RegisterForm from './components/RegisterForm.vue'
import LoginForm from './components/LoginForm.vue'

const routes = [
  { path: '/', component: CommentPage },
  { path: '/register', component: RegisterForm },
  { path: '/login', component: LoginForm },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
