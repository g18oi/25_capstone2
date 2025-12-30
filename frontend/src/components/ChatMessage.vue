<template>
  <div class="msg-row" :class="{ mine: isMine }">
    <div class="bubble">
      <div class="text">{{ message.text }}</div>
      <div class="time">{{ message.time }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatMessage',
  props: {
    message: {
      type: Object,
      required: true
    },
    myId: {
      type: String,
      required: true
    }
  },
  computed: {
    isMine() {
      return this.message.senderId === this.myId
    }
  }
}
</script>

<style scoped>
.msg-row {
  display: flex;
  margin: 8px 0;
}

.msg-row.mine {
  justify-content: flex-end;
}

.bubble {
  max-width: 70%;
  background: white;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 10px 12px;
}

.msg-row.mine .bubble {
  background: #fff7e6;
  border-color: #ffe1a3;
}

.text {
  line-height: 1.4;
}

.time {
  font-size: 11px;
  color: #999;
  margin-top: 6px;
  text-align: right;
}
</style>
