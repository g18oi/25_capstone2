<template>
  <div class="chat-page">
    <TheHeader />

    <main class="chat-container">
      <ChatRoomHeader :otherName="otherName" />

      <div class="chat-body" ref="chatBody">
        <div v-if="isLoading" class="loading">메시지 로딩 중...</div>
        <ChatMessage
          v-for="(msg, index) in messages"
          :key="index"
          :message="msg"
          :myId="myId"
        />
      </div>

      <ChatInput @send="sendMessage" />
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import TheHeader from '@/components/TheHeader.vue'
import ChatRoomHeader from '@/components/ChatRoomHeader.vue'
import ChatMessage from '@/components/ChatMessage.vue'
import ChatInput from '@/components/ChatInput.vue'

export default {
  name: 'ChatView',
  components: { TheHeader, ChatRoomHeader, ChatMessage, ChatInput },
  data() {
    return {
      roomId: null,
      myId: null,
      otherName: '상대방',
      messages: [],
      socket: null,
      isLoading: false
    }
  },
  async mounted() {
    this.roomId = this.$route.params.roomId
    
    await this.fetchMyInfo();


    if (this.myId) {
      this.fetchHistory();
      this.connectWebSocket();
    } else {
      alert("사용자 정보를 불러오지 못했습니다. 다시 로그인해주세요.");
      this.$router.push('/login');
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    async fetchMyInfo() {
        try {
            const token = localStorage.getItem('token');
            if (!token) throw new Error("토큰 없음");

            const res = await axios.get('/api/user/me', {
                headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
            });
            this.myId = res.data.id;
        } catch(e) {
            console.error("내 정보 로드 실패", e);
        }
    },
    async fetchHistory() {
      this.isLoading = true;
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`/chat/history/${this.roomId}`, {
           headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        
        console.log("서버가 보낸 히스토리 데이터:", res.data);
        const historyList = Array.isArray(res.data) ? res.data : [];
        if (!Array.isArray(res.data)) {
        console.warn("주의: 서버 응답이 리스트가 아닙니다! (HTML이나 에러 메시지일 수 있음)");
        
  
        this.messages = historyList.map(m => ({ 
          id: m.id,
          senderId: m.sender_id,
          text: m.content,
          time: m.timestamp ? new Date(m.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''
}))}
        
        this.$nextTick(this.scrollToBottom);
      } catch (error) {
        console.error("채팅 내역 로드 실패:", error);
      } finally {
        this.isLoading = false;
      }
    },
connectWebSocket() {
      if(!this.myId) return;

      const token = localStorage.getItem('token'); 

      const backendUrl = "9cf4e2ebac00.ngrok-free.app"; 
      const protocol = backendUrl.includes("ngrok") || backendUrl.includes("vercel") ? "wss:" : "ws:";
      

      const wsUrl = `${protocol}//${backendUrl}/chat/ws/${this.roomId}/${this.myId}?token=${token}`;
      
      console.log("WebSocket 연결 시도:", wsUrl);

      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
          console.log("웹소켓 연결 성공!");
      };

      this.socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.messages.push({
              senderId: data.sender_id,
              text: data.content,
              time: new Date(data.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
          });
          this.$nextTick(this.scrollToBottom);
      };

      this.socket.onclose = () => {
          console.log("웹소켓 연결 종료");
      };
      
      this.socket.onerror = (error) => {
          console.error("웹소켓 에러 발생:", error);
      };
  },
    sendMessage(text) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const msg = { content: text }; 
        this.socket.send(JSON.stringify(msg));
      } else {
        alert("연결이 끊어졌습니다. 페이지를 새로고침 해주세요.");
      }
    },
    scrollToBottom() {
      const el = this.$refs.chatBody
      if (el) el.scrollTop = el.scrollHeight
    }
  }
}
</script>
<style scoped>
.chat-page {
  background: #f8f9fa;
  min-height: 100vh;
}

.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background: white;
  border-left: 1px solid #eee;
  border-right: 1px solid #eee;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
}
</style>