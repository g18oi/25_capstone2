<template>
  <form class="chat-input" @submit.prevent="submit">
    <input
      v-model="draft"
      type="text"
      placeholder="메시지를 입력하세요…"
    />
    <button type="submit" :disabled="!draft.trim()">전송</button>
  </form>
</template>

<script>
export default {
  name: 'ChatInput',
  emits: ['send'],
  data() {
    return {
      draft: ''
    }
  },
  methods: {
    submit() {
      if (!this.draft.trim()) return
      this.$emit('send', this.draft)
      this.draft = ''
    }
  }
}
</script>

<style scoped>
.chat-input {
  display: flex;
  gap: 10px;
  padding: 12px;
  border-top: 1px solid #eee;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
}

.chat-input button {
  border: none;
  border-radius: 10px;
  padding: 0 16px;
  font-weight: 800;
  background: #FBBF24;
  cursor: pointer;
}
</style>
