<template>
  <div class="auth-wrapper">
    <form @submit.prevent="register" class="auth-form">
      <h2 class="register-title">Реєстрація</h2>
      <input v-model="username" placeholder="Імя користувача" required />
      <input v-model="email" placeholder="Email" type="email" required />
      <input v-model="password" placeholder="Пароль" type="password" required />
      <button type="submit">Зареєструватися</button>
      <p class="message" v-if="message">{{ message }}</p>
      <router-link to="/login">Вже є аккаунт? Ввійти</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const message = ref('');

async function register() {
  message.value = '';

  try {
    const res = await fetch('/api/auth/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value
      })
    });

    if (res.ok) {
      message.value = 'Ви успішно зареєструвались! Зараз ви будете перенаправлені на вхід...';
      setTimeout(() => router.push('/login'), 2000);
    } else {
      const text = await res.text(); // читаем текст, а не json
      try {
        const data = JSON.parse(text);
        message.value = 'Помилка: ' + (data.detail || JSON.stringify(data));
      } catch {
        message.value = 'Помилка: ' + text;
      }
    }
  } catch (err) {
    console.error('Помилка мережі чи JS:', err);
    message.value = "Помилка мережі. Перевірте з'єднання.";
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
  background: #388e3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.auth-form button:hover {
  background: #2e7d32;
}
.message {
  color: green;
  margin-top: 10px;
}
</style>
