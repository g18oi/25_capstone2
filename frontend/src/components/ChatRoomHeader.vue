<template>
  <div class="chat-room-header">
    <button class="back-btn" @click="$router.back()">←</button>

    <div class="room-title">
      <div class="name">{{ otherName }}</div>
      <div class="sub">1:1 채팅</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatRoomHeader',
  props: {
    otherName: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.chat-room-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid #eee;
  background: white;
}

.back-btn {
  border: none;
  background: none;
  font-size: 18px;
  cursor: pointer;
}

.room-title .name {
  font-weight: 800;
}

.room-title .sub {
  font-size: 12px;
  color: #888;
}
</style>
