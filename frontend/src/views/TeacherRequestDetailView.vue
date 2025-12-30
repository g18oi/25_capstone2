<template>
  <div class="page-container">
    <TheHeader />
    <main class="main-container">
      
      <div v-if="isLoading" class="loading">불러오는 중...</div>

      <div class="detail-card" v-else-if="requestData">
        <div class="card-header">
          <span class="badge">요청서</span>
          <h2>{{ requestData.parent_name }} 학부모님의 요청</h2>
        </div>

        <div class="info-section">
          <div class="info-row">
            <span class="label">📍 위치</span>
            <span class="value">{{ requestData.location }}</span>
          </div>
          <div class="info-row">
            <span class="label">⏰ 시간</span>
            <span class="value">{{ requestData.start_time }} ({{ requestData.duration }})</span>
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
            <span class="value requirements">{{ requestData.requirements }}</span>
          </div>
        </div>

        <div class="btn-group" v-if="requestData.status === 'pending'">
          <button class="back-btn" @click="$router.go(-1)">뒤로가기</button>
          <button class="reject-btn" @click="handleResponse(false)">거절하기</button>
          <button class="accept-btn" @click="handleResponse(true)">수락하기</button>
        </div>
        <div class="status-msg" v-else>
            이미 <strong>{{ requestData.status }}</strong> 처리된 요청입니다.
            <button class="back-btn" @click="$router.go(-1)" style="margin-left: 10px;">목록으로</button>
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
import axios from 'axios';
import TheHeader from '@/components/TheHeader.vue';

export default {
  components: { TheHeader },
  data() {
    return {
      requestData: null,
      isLoading: false
    };
  },
  mounted() {
    const id = this.$route.params.id;
    this.fetchDetail(id);
  },
  methods: {
    async fetchDetail(id) {
        this.isLoading = true;
        try {
            const token = localStorage.getItem('token');
            const res = await axios.get(`/api/match/${id}`, {
                headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
            });
            this.requestData = res.data;
        } catch (error) {
            console.error("상세 정보 로드 실패:", error);
            alert("정보를 불러오지 못했습니다.");
        } finally {
            this.isLoading = false;
        }
    },
    formatPay(pay) {
      return pay ? Number(pay).toLocaleString() : '0';
    },
    async handleResponse(accept) {
      if(!confirm(accept ? '이 요청을 수락하시겠습니까?' : '정말 거절하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.post('/api/match/response', null, {
            params: { 
                match_id: this.requestData.id,
                accept: accept 
            },
            headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });

        alert(accept ? '수락되었습니다! 채팅방이 생성됩니다.' : '거절 처리되었습니다.');
        this.$router.push('/teacher-home');

      } catch (error) {
        console.error("응답 처리 실패:", error);
        alert("처리 중 오류가 발생했습니다.");
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