<template>
  <div class="page-container">
    <TheHeader />
    <main class="main-container">
      
      <div class="detail-card" v-if="requestData">
        <div class="card-header">
          <span class="badge">모집중</span>
          <h2>{{ requestData.parent_name }} 학부모님의 요청</h2>
        </div>

        <div class="info-section">
          <div class="info-row">
            <span class="label">📍 위치</span>
            <span class="value">{{ requestData.location }}</span>
          </div>
          <div class="info-row">
            <span class="label">⏰ 시간</span>
            <span class="value">{{ requestData.start_time }} ({{ requestData.duration }}시간)</span>
          </div>
          <div class="info-row">
            <span class="label">💰 시급</span>
            <span class="value highlight">{{ formatPay(requestData.hourly_pay) }}원</span>
          </div>
          <div class="info-row">
            <span class="label">👶 아이 정보</span>
            <span class="value">{{ requestData.children_info }}</span>
          </div>
          <div class="info-row">
            <span class="label">📝 요청 사항</span>
            <span class="value">{{ requestData.requirements }}</span>
          </div>
        </div>

        <div class="btn-group">
          <button class="back-btn" @click="$router.go(-1)">목록으로</button>
          <button class="reject-btn" @click="rejectRequest">거절하기</button>
          <button class="accept-btn" @click="acceptRequest">수락하기</button>
        </div>
      </div>

      <div v-else class="error-msg">
        <p>요청 정보를 찾을 수 없습니다.</p>
        <button @click="$router.push('/teacher-home')">홈으로 돌아가기</button>
      </div>

    </main>
  </div>
</template>

<script>
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { TheHeader },
  data() {
    return {
      requestData: null,
      allRequests: [
        {
          id: 1,
          parent_name: '이영희',
          location: '서울 강남구 역삼동',
          start_time: '14:00:00',
          duration: 3,
          hourly_pay: 15000,
          created_at: '2025-12-20T09:00:00',
          children_info: '7세 남아 (활동적임)',
          requirements: '영어 놀이를 위주로 부탁드려요.'
        },
        {
          id: 2,
          parent_name: '박철수',
          location: '서울 서초구 반포동',
          start_time: '10:00:00',
          duration: 4,
          hourly_pay: 18000,
          created_at: '2025-12-21T11:00:00',
          children_info: '5세 여아 (낯가림 있음)',
          requirements: '책 읽어주기를 좋아해요. 차분하게 놀아주세요.'
        }
      ]
    };
  },
  mounted() {
    const id = parseInt(this.$route.params.id);
    this.requestData = this.allRequests.find(req => req.id === id);

    if (!this.requestData) {
      console.error("해당 ID의 요청을 찾을 수 없습니다:", id);
    }
  },
  methods: {
    formatPay(pay) {
      return pay ? pay.toLocaleString() : '0';
    },
    acceptRequest() {
      if(!this.requestData) return;
      if(confirm('이 요청을 수락하시겠습니까?')) {
        alert(`${this.requestData.parent_name}님의 요청을 수락했습니다!\n(채팅방이 생성됩니다)`);
        this.$router.push('/teacher-home');
      }
    },
    rejectRequest() {
      if(!this.requestData) return;
      if(confirm('정말 거절하시겠습니까?')) {
        alert('거절 처리되었습니다.');
        this.$router.push('/teacher-home');
      }
    }
  }
};
</script>

<style scoped>
.page-container { background-color: #f8f9fa; min-height: 100vh; }
.main-container { max-width: 600px; margin: 0 auto; padding: 40px 20px; }

.detail-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.card-header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
.badge { background-color: #E3F2FD; color: #1976D2; padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }
.card-header h2 { margin: 15px 0 0 0; color: #333; font-size: 1.4rem; }

.info-section { margin-bottom: 30px; }
.info-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5; font-size: 0.95rem; }
.info-row:last-child { border-bottom: none; }
.label { color: #888; font-weight: 500; }
.value { color: #333; font-weight: 600; text-align: right; max-width: 70%; word-break: keep-all; }
.value.highlight { color: #2E7D32; font-size: 1.1rem; }

.btn-group { display: flex; gap: 10px; }
.back-btn { flex: 1; padding: 15px; border-radius: 12px; border: 1px solid #ddd; background: white; color: #666; font-weight: bold; cursor: pointer; }


.reject-btn { flex: 2; padding: 15px; border-radius: 12px; border: none; background: #FFEBEE; color: #D32F2F; font-weight: bold; cursor: pointer; font-size: 1rem; }
.accept-btn { flex: 2; padding: 15px; border-radius: 12px; border: none; background: #4CAF50; color: white; font-weight: bold; cursor: pointer; font-size: 1rem; }

.back-btn:hover { background-color: #f5f5f5; }
.reject-btn:hover { background-color: #FFCDD2; }
.accept-btn:hover { background-color: #43A047; }

.error-msg { text-align: center; padding: 50px; color: #888; }
</style>