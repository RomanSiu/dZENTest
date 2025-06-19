<template>
  <form class="comment-form" @submit.prevent="handleSubmit">
    <textarea
      v-model="text"
      placeholder="Ваш коментар..."
      required
    ></textarea>

    <img :src="captcha.image_url" alt="captcha" />
    <input v-model="captchaText" placeholder="Введіть CAPTCHA" />

    <div class="file-group">
      <label>
        📷 Фото:
        <input type="file" accept="image/png,image/jpeg,image/gif" @change="handleImage" />
      </label>
      <label>
        📄 Файл:
        <input type="file" accept="text/plain" @change="handleTextFile" />
      </label>
    </div>

    <button type="submit">Відправити</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const emit = defineEmits(['submitted'])
const props = defineProps({
  parentId: Number
})

const text = ref('')
const imageFile = ref(null)
const textFile = ref(null)
const captcha = ref({})
const captchaText = ref('')

function handleImage(e) {
  const file = e.target.files[0]
  if (file && file.size > 0) {
    const img = new Image()
    const reader = new FileReader()
    reader.onload = event => {
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const maxW = 320
        const maxH = 240
        let { width, height } = img

        if (width > maxW || height > maxH) {
          const scale = Math.min(maxW / width, maxH / height)
          width *= scale
          height *= scale
        }
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)
        canvas.toBlob(blob => {
          imageFile.value = new File([blob], file.name, { type: file.type })
        }, file.type)
      }
      img.src = event.target.result
    }
    reader.readAsDataURL(file)
  }
}

function handleTextFile(e) {
  const file = e.target.files[0]
  if (file && file.size <= 102400) {
    textFile.value = file
  } else {
    alert('Файл повинен бути формата .txt та не більше 100 кб')
    e.target.value = ''
  }
}

async function handleSubmit() {
  const formData = new FormData()
  formData.append('text', text.value)
  if (props.parentId) {
    formData.append('parent', props.parentId)
  }
  if (imageFile.value) {
    formData.append('attachments', imageFile.value)
  }
  if (textFile.value) {
    formData.append('attachments', textFile.value)
  }
  formData.append('captcha_key', captcha.value.key)
  formData.append('captcha_text', captchaText.value)

  const res = await fetch('/api/comments/add/', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt_access')}`
    },
    body: formData
  })

  if (res.ok) {
    text.value = ''
    imageFile.value = null
    textFile.value = null
    emit('submitted')
  } else {
    const err = await res.json()
    alert('Помилка відправки: ' + JSON.stringify(err))
  }
}

async function loadCaptcha() {
  const res = await fetch('http://localhost:8000/api/comments/captcha/')
  captcha.value = await res.json()
}

onMounted(loadCaptcha)
</script>

<style scoped>
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 15px;
}

textarea {
  min-height: 80px;
  padding: 10px;
  resize: vertical;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.file-group label {
  display: block;
  margin-bottom: 5px;
}

button {
  background: #1976d2;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background: #125ca1;
}
</style>
