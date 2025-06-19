<template>
  <div class="comment-list">
    <div
      v-for="comment in comments"
      :key="comment.id"
      class="comment-item"
    >
      <div class="comment-content">
        <p class="meta">
          <strong>{{ comment.username }}</strong>
          <span>&lt;{{ comment.email }}&gt;</span>
          <span class="date">{{ formatDate(comment.created_at) }}</span>
        </p>
        <p class="text" v-html="sanitize(comment.text)"></p>

        <div v-if="comment.attachments">
          <div v-for="file in comment.attachments" :key="file.id">
            <a :href="file.file" target="_blank">📎 {{ file.name }}</a>
            <img v-if="file.file.endsWith('.jpg') || file.file.endsWith('.png')"
                 :src="file.file"
                 style="max-width: 200px; display: block; margin-top: 5px" />
          </div>
        </div>

        <button class="reply-btn" @click="toggleReply(comment.id)">
          Ответить
        </button>
      </div>

      <CommentForm
        v-if="activeReply === comment.id"
        :parentId="comment.id"
        @submitted="handleSubmitted"
      />

      <div class="child-comments">
        <CommentList
          v-if="comment.replies && comment.replies.length"
          :comments="comment.replies"
          @submitted="handleSubmitted"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comments: Array
})
const emit = defineEmits(['submitted'])

const activeReply = ref(null)

function toggleReply(id) {
  activeReply.value = activeReply.value === id ? null : id
}

function handleSubmitted() {
  emit('submitted')
  activeReply.value = null
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}

function sanitize(text) {
  const allowedTags = ['a', 'code', 'i', 'strong']
  const div = document.createElement('div')
  div.innerHTML = text

  const walker = document.createTreeWalker(div, NodeFilter.SHOW_ELEMENT, null, false)

  const nodesToRemove = []

  while (walker.nextNode()) {
    const el = walker.currentNode
    if (!allowedTags.includes(el.tagName.toLowerCase())) {
      nodesToRemove.push(el)
    }
  }

  for (const el of nodesToRemove) {
    const parent = el.parentNode
    if (parent) {
      while (el.firstChild) {
        parent.insertBefore(el.firstChild, el)
      }
      parent.removeChild(el)
    }
  }

  return div.innerHTML
}
</script>

<style scoped>
.comment-list {
  margin-left: 0;
}

.comment-item {
  padding: 10px;
  border-left: 3px solid #1976d2;
  margin-bottom: 15px;
}

.comment-content {
  background: #f4f6fa;
  padding: 10px;
  border-radius: 6px;
}

.meta {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.date {
  margin-left: auto;
  font-style: italic;
}

.text {
  margin: 10px 0;
  white-space: pre-line;
}

.reply-btn {
  background: transparent;
  color: #1976d2;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  font-size: 0.9em;
}

.reply-btn:hover {
  text-decoration: underline;
}

.child-comments {
  margin-left: 25px;
  margin-top: 10px;
}
</style>
