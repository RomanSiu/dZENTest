<template>
  <div class="auth-wrapper">
    <form @submit.prevent="login" class="auth-form">
      <h2 class="login-title">Вхід</h2>
      <input v-model="username" placeholder="Імя користувача" required />
      <input v-model="password" placeholder="Пароль" type="password" required />
      <button type="submit">Ввійти</button>
      <p class="message" v-if="message">{{ message }}</p>
      <router-link to="/register">Нема аккаунту? Зареєструватися</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')

async function login() {
  const res = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username.value, password: password.value })
  })

  if (res.ok) {
    const data = await res.json()
    localStorage.setItem('jwt_access', data.access)
    localStorage.setItem('jwt_refresh', data.refresh)
    message.value = 'Ви успішно ввійшли!'
    setTimeout(() => router.push('/'), 1000)
  } else {
    const data = await res.json()
    message.value = 'Помилка входу: ' + (data.detail || 'Неправильні данні')
  }
}
</script>

<style scoped>
.auth-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 50px;
}
.auth-form {
  width: 300px;
  padding: 20px;
  border: 1px solid #ddd;
  background: #f9f9f9;
  border-radius: 8px;
}
.auth-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.auth-form button {
  width: 100%;
  padding: 10px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.auth-form button:hover {
  background: #125ca1;
}
.message {
  color: green;
  margin-top: 10px;
}
</style>


