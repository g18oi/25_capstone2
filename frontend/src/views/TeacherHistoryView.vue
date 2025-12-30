<template>
  <div class="manage-page">
    <TheHeader />

    <main class="manage-container">
      <div class="page-header">
        <h1>📨 내 돌봄 내역 (선생님)</h1>
      </div>

      <div class="tabs">
        <button :class="{ active: currentFilter === 'all' }" @click="currentFilter = 'all'">전체</button>
        <button :class="{ active: currentFilter === 'pending' }" @click="currentFilter = 'pending'">대기중</button>
        <button :class="{ active: currentFilter === 'accepted' }" @click="currentFilter = 'accepted'">진행/완료</button>
      </div>

      <div v-if="isLoading" class="msg">내역을 불러오는 중입니다...</div>
      <div v-else-if="filteredRequests.length === 0" class="msg">해당하는 내역이 없습니다.</div>

      <div v-else class="request-list">
        <div
          v-for="req in filteredRequests"
          :key="req.match_id"
          class="request-card"
          :class="{ highlight: req.status === 'pending' }"
        >
          <div class="card-content" @click="goToDetail(req.match_id)">
            <div class="card-header">
              <span class="parent-name">{{ req.parent_name }} 학부모님</span>
              <span :class="['status-badge', req.status]">{{ formatStatus(req.status) }}</span>
            </div>
            <p class="details">📍 {{ req.location || '지역 정보 없음' }}</p>
            <p class="details">💰 {{ formatPay(req.hourly_pay) }}원/시</p>
            <p class="date">{{ formatDate(req.created_at) }} 신청됨</p>
          </div>

          <div class="card-actions" v-if="req.status !== 'pending' && req.status !== 'rejected'">
            <button class="btn-action chat" @click.stop="openChat(req.match_id)">
              💬 채팅하기
            </button>
            <button class="btn-action report" @click.stop="openReport(req)">
              🚨 신고하기
            </button>
          </div>
        </div>
      </div>
      
      <ReportModal
        :isVisible="reportModal.visible"
        :targetName="reportModal.targetName"
        :targetId="reportModal.targetId"
        @close="closeReportModal"
      />

    </main>
  </div>
</template>

<script>
import axios from 'axios';
import TheHeader from '@/components/TheHeader.vue';
import ReportModal from '@/components/ReportModal.vue';

export default {
  components: { TheHeader, ReportModal },
  data() {
    return {
      isLoading: false,
      requests: [],
      currentFilter: 'all',
      reportModal: {
        visible: false,
        targetName: '',
        targetId: null
      }
    };
  },
  computed: {
    filteredRequests() {
      if (this.currentFilter === 'all') return this.requests;
      if (this.currentFilter === 'pending') return this.requests.filter(r => r.status === 'pending');
      if (this.currentFilter === 'accepted') return this.requests.filter(r => ['accepted', 'completed'].includes(r.status));
      return this.requests;
    }
  },
  mounted() {
    this.fetchHistory();
  },
  methods: {
    async fetchHistory() {
      this.isLoading = true;
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/match/sitter/list', {
           headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        this.requests = res.data;
      } catch (error) {
        console.error("내역 로드 실패:", error);
      } finally {
        this.isLoading = false;
      }
    },
    formatStatus(status) {
      const map = { 
        'pending': '대기중', 
        'accepted': '진행중', 
        'rejected': '거절됨', 
        'completed': '종료됨' 
      };
      return map[status] || status;
    },
    formatPay(pay) {
      return pay ? Number(pay).toLocaleString() : '0';
    },
    formatDate(dateStr) {
      if(!dateStr) return '';
      return dateStr.split('T')[0];
    },
    goToDetail(id) {
      this.$router.push(`/teacher/request/${id}`);
    },
    openChat(matchId) {
      this.$router.push(`/chat/${matchId}`);
    },
    openReport(req) {
      this.reportModal.targetName = req.parent_name;
      this.reportModal.targetId = req.match_id;
      this.reportModal.visible = true;
    },
    closeReportModal() {
      this.reportModal.visible = false;
    }
  }
};
</script>

<style scoped>
.manage-page { background-color: #f8f9fa; min-height: 100vh; }
.manage-container { max-width: 600px; margin: 0 auto; padding: 20px; }

.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: #eee;
  border-radius: 8px;
  font-weight: bold;
}
.tabs button.active {
  background: #4CAF50;
  color: white;
}

.request-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  border: 1px solid #eee;
}
.request-card.highlight {
  border: 2px solid #FF9800;
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}
.parent-name { font-weight: bold; }

.btn-chat {
  margin-top: 10px;
  background: none;
  border: none;
  color: #F59E0B;
  font-weight: bold;
  cursor: pointer;
}
.btn-chat:hover {
  text-decoration: underline;
}

.btn-report {
  margin-top: 10px;
  background: none;
  border: none;
  color: #ff4d4f;
  font-weight: bold;
  cursor: pointer;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}
.btn-accept {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 8px;
}
.btn-reject {
  background: #ffebee;
  color: #d32f2f;
  border: none;
  padding: 10px;
  border-radius: 8px;
}

.status-msg {
  margin-top: 15px;
  text-align: center;
  color: #888;
}
.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #888;
}
</style>
