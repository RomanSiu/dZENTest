<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-item">Главная</router-link>
        <router-link to="/login" class="nav-item">Вход</router-link>
        <router-link to="/register" class="nav-item">Регистрация</router-link>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// App.vue — layout с навигацией
</script>

<style scoped>
body {
  font-family: 'Segoe UI', sans-serif;
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background: #f5f6fa;
  color: #333;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #1976d2;
  border-bottom: 1px solid #1976d2;
  padding: 12px 20px;
  display: flex;
  gap: 20px;
  z-index: 10;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-item:hover {
  text-decoration: underline;
}

.main-content {
  padding-top: 60px;
  min-height: calc(100vh - 60px);
  background-color: #fff;
  height: 100%;
  width: 100%;
  padding-left: 20px;
  padding-right: 20px;
}
</style>