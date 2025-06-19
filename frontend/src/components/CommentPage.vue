<template>
  <div class="comment-page">
    <button class="add-comment-btn" @click="showForm = !showForm">
      {{ showForm ? 'Закрити' : 'Додати коментар' }}
    </button>

    <div class="sort-bar">
      <label for="sort">Сортувати за:</label>
      <select v-model="sort" @change="fetchComments">
        <option value="username">імя</option>
        <option value="email">Email</option>
        <option value="created_at">Дата</option>
      </select>

      <button @click="toggleOrder">
        {{ order === 'desc' ? '↓' : '↑' }}
      </button>
    </div>

    <CommentForm v-if="showForm" @submitted="handleSubmitted" />

    <CommentList
      v-if="comments.length > 0"
      :comments="comments"
      @submitted="handleSubmitted"
    />

    <p v-else class="no-comments">Коментарів поки немає</p>

    <div class="pagination">
      <button @click="prevPage" :disabled="!prev" class="page-btn">← Назад</button>
      <span>Сторінка {{ page }}</span>
      <button @click="nextPage" :disabled="!next" class="page-btn">Вперед →</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommentForm from './CommentForm.vue'
import CommentList from './CommentList.vue'

const showForm = ref(false)
const comments = ref([])
const page = ref(1)
const sort = ref('created_at')
const order = ref('desc')
const next = ref(null)
const prev = ref(null)


async function loadComments() {
  try {
    const res = await fetch('/api/comments/')
    if (res.ok) {
      const data = await res.json()
      comments.value = data.results
    } else {
      console.error('Помилка завантаження коментарів')
    }
  } catch (err) {
    console.error('Помилка:', err)
  }
}

async function fetchComments() {
  const res = await fetch(
    `http://localhost:8000/api/comments/?sort=${sort.value}&order=${order.value}&page=${page.value}`
  )
  const data = await res.json()
  comments.value = data.results
  next.value = data.next
  prev.value = data.previous
}

function nextPage() {
  page.value++
  fetchComments()
}

function prevPage() {
  page.value--
  fetchComments()
}

function toggleOrder() {
  order.value = order.value === 'desc' ? 'asc' : 'desc'
  fetchComments()
}

onMounted(fetchComments)


function handleSubmitted() {
  loadComments()
  showForm.value = false
}

onMounted(loadComments)
</script>

<style scoped>
.comment-page {
  padding: 20px;
  width: 100%;
  max-width: none;
}

.add-comment-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 15px;
}

.add-comment-btn:hover {
  background-color: #125ca1;
}

.no-comments {
  color: #888;
  font-style: italic;
}

.sort-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  color: #888;
}
.sort-bar select, .sort-bar button {
  padding: 5px 10px;
  font-size: 0.9em;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
}

.page-btn {
  padding: 6px 12px;
  font-size: 0.9em;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>

