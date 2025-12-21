<template>
  <div class="manage-page">
    <TheHeader />

    <main class="manage-container">
      <div class="page-header">
        <h1>📨 받은 돌봄 신청 내역</h1>
        <p>선생님에게 들어온 의뢰를 관리해보세요.</p>
      </div>

      <div class="tabs">
        <button :class="{ active: currentFilter === 'all' }" @click="currentFilter = 'all'">전체</button>
        <button :class="{ active: currentFilter === 'pending' }" @click="currentFilter = 'pending'">대기중 🔥</button>
        <button :class="{ active: currentFilter === 'confirmed' }" @click="currentFilter = 'confirmed'">확정됨</button>
      </div>

      <div class="request-list">
        <div
          v-for="req in filteredRequests"
          :key="req.id"
          class="request-card"
          :class="{ highlight: req.status === 'pending' }"
        >
          <div class="card-header">
            <span class="parent-name">{{ req.parentName }} 학부모님</span>
            <span :class="['status-badge', req.status]">
              {{ getStatusText(req.status) }}
            </span>
          </div>

          <div class="card-body">
            <p><strong>📅 일시:</strong> {{ req.date }} / {{ req.time }}</p>
            <p><strong>📍 장소:</strong> {{ req.location }}</p>
            <p><strong>💰 수익금:</strong> {{ req.pay.toLocaleString() }}원</p>
          </div>

          <button class="btn-report" @click="openReportModal(req)">
            🚨 학부모 신고하기
          </button>

          <div v-if="req.status === 'pending'" class="action-buttons">
            <button class="btn-reject" @click="handleReject(req.id)">거절</button>
            <button class="btn-accept" @click="handleAccept(req.id)">수락</button>
          </div>

          <div v-else class="status-msg">
            {{ req.status === 'in-progress'
              ? '✅ 매칭되어 진행 중입니다.'
              : '❌ 거절/취소된 건입니다.' }}
          </div>
        </div>

        <div v-if="filteredRequests.length === 0" class="empty-state">
          <p>해당하는 신청 내역이 없습니다.</p>
        </div>
      </div>
    </main>

    <Teleport to="body">
      <ReportModal
        :isVisible="reportModal.visible"
        :targetName="reportModal.targetName"
        :targetId="reportModal.targetId"
        @close="closeReportModal"
      />
    </Teleport>
  </div>
</template>

<script>
import TheHeader from '@/components/TheHeader.vue'
import ReportModal from '@/components/ReportModal.vue'

export default {
  components: { TheHeader, ReportModal },
  data() {
    return {
      currentFilter: 'all',

      requests: [
        {
          id: 1,
          parentName: '이영희',
          status: 'pending',
          date: '2025.10.20',
          time: '14:00 (3시간)',
          location: '서울 강남구 역삼동',
          pay: 45000
        },
        {
          id: 2,
          parentName: '박철수',
          status: 'in-progress',
          date: '2025.10.18',
          time: '10:00 (2시간)',
          location: '서울 서초구 반포동',
          pay: 30000
        },
        {
          id: 3,
          parentName: '최민수',
          status: 'rejected',
          date: '2025.10.15',
          time: '09:00 (4시간)',
          location: '서울 송파구 잠실동',
          pay: 60000
        }
      ],

      reportModal: {
        visible: false,
        targetName: '',
        targetId: null
      }
    }
  },
  computed: {
    filteredRequests() {
      if (this.currentFilter === 'all') return this.requests
      if (this.currentFilter === 'pending') return this.requests.filter(r => r.status === 'pending')
      if (this.currentFilter === 'confirmed') return this.requests.filter(r => r.status === 'in-progress')
      return this.requests
    }
  },
  methods: {
    getStatusText(status) {
      const map = {
        pending: '수락 대기',
        'in-progress': '매칭 확정',
        rejected: '거절됨'
      }
      return map[status] || status
    },

    handleAccept(id) {
      if (confirm('수락하시겠습니까?')) {
        const item = this.requests.find(r => r.id === id)
        if (item) item.status = 'in-progress'
      }
    },

    handleReject(id) {
      if (confirm('거절하시겠습니까?')) {
        const item = this.requests.find(r => r.id === id)
        if (item) item.status = 'rejected'
      }
    },

    openReportModal(req) {
      this.reportModal.targetName = req.parentName
      this.reportModal.targetId = req.id
      this.reportModal.visible = true
    },
    closeReportModal() {
      this.reportModal.visible = false
      this.reportModal.targetName = ''
      this.reportModal.targetId = null
    }
  }
}
</script>

<style scoped>
.manage-page { background-color: #f8f9fa; min-height: 100vh; }
.manage-container { max-width: 600px; margin: 0 auto; padding: 20px; }
.page-header h1 { font-size: 1.4rem; margin-bottom: 5px; }
.page-header p { color: #666; margin-bottom: 20px; }

.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tabs button { flex: 1; padding: 10px; border: none; background: #eee; border-radius: 8px; font-weight: bold; }
.tabs button.active { background: #4CAF50; color: white; }

.request-card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; border: 1px solid #eee; }
.request-card.highlight { border: 2px solid #FF9800; }

.card-header { display: flex; justify-content: space-between; margin-bottom: 15px; }
.parent-name { font-weight: bold; }

.btn-report {
  margin-top: 10px;
  background: none;
  border: none;
  color: #ff4d4f;
  font-weight: bold;
  cursor: pointer;
}

.action-buttons { display: flex; gap: 10px; margin-top: 15px; }
.btn-accept { background: #4CAF50; color: white; border: none; padding: 10px; border-radius: 8px; }
.btn-reject { background: #ffebee; color: #d32f2f; border: none; padding: 10px; border-radius: 8px; }

.status-msg { margin-top: 15px; text-align: center; color: #888; }
.empty-state { text-align: center; padding: 40px 0; color: #888; }
</style>
