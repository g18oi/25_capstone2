<template>
  <div class="history-page">
    <TheHeader />
    <main class="history-container">
      <h1>나의 돌봄 내역 (학부모용)</h1>

      <div v-if="isLoading" class="loading-msg">내역을 불러오는 중...</div>
      <div v-else-if="careHistory.length === 0" class="empty-msg">아직 돌봄 내역이 없습니다.</div>

      <div v-else v-for="item in careHistory" :key="item.match_id" class="care-item">
        <div class="item-header">
          <span class="teacher-name">{{ item.sitter_name }} 선생님과의 돌봄</span>
          <span :class="['status', getStatusClass(item.status)]">{{ formatStatus(item.status) }}</span>
        </div>

        <p class="item-period">{{ formatDate(item.created_at) }} 신청</p>

        <div
          v-if="reviewForm.visible && reviewForm.targetId === item.match_id"
          class="review-form-wrapper"
        >
          <hr />
          <div class="review-form">
            <h4>{{ item.has_review ? '후기 수정하기' : '새 후기 작성' }}</h4>

            <div class="detailed-ratings">
              <div
                v-for="category in ratingCategories"
                :key="category.key"
                class="rating-item"
              >
                <label>{{ category.label }}</label>
                <div class="star-rating">
                  <span
                    v-for="n in 5"
                    :key="n"
                    @click="setDetailedRating(category.key, n)"
                  >
                    {{ n <= reviewForm.ratings[category.key] ? '★' : '☆' }}
                  </span>
                </div>
              </div>
            </div>

            <div class="input-group">
              <label>선생님과의 경험을 공유해주세요.</label>
              <textarea
                v-model="reviewForm.text"
                placeholder="솔직한 후기를 남겨주세요."
              ></textarea>
            </div>

            <div class="btn-group">
              <BaseButton type="outline" @click="closeReviewForm">
                닫기
              </BaseButton>
              <BaseButton type="primary" @click="submitReview()">
                {{ item.has_review ? '수정 완료' : '후기 등록' }}
              </BaseButton>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <button class="btn-report" @click="openReportModal(item)">
            🚨 신고하기
          </button>

          <div class="right-actions">
            <button class="btn-chat" @click="openChat(item)">
              💬 채팅하기
            </button>

            <span v-if="item.status === 'pending'" class="pending-msg">
              ⏳ 선생님 수락 대기 중
            </span>

            <button
              v-else-if="(item.status === 'completed' || item.status === '종료됨') && item.has_review"
              class="btn-text-action"
              @click="openReviewForm(item)"
            >
              📝 내 후기 보기/수정
            </button>

            <BaseButton
              v-else-if="(item.status === 'completed' || item.status === '종료됨') && !item.has_review"
              type="secondary"
              @click="openReviewForm(item)"
            >
              후기 등록
            </BaseButton>

            <span v-else-if="item.status === 'accepted' || item.status === '진행중'" class="ing-msg">
              현재 돌봄 진행 중
            </span>

            <span v-else-if="item.status === 'rejected'" class="rej-msg">
               선생님이 거절했습니다
            </span>
          </div>
        </div>
      </div>

      <ReportModal
        :isVisible="reportModal.visible"
        :targetName="reportModal.targetName"
        :targetId="reportModal.targetId"
        @close="closeReportModal"
      />

      <GlobalModal
        :visible="rejectModal.visible"
        :message="rejectModal.message"
        @close="closeRejectModal"
        @confirm="confirmRejectModal"
      />
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import BaseButton from '../components/BaseButton.vue'
import TheHeader from '../components/TheHeader.vue'
import ReportModal from '@/components/ReportModal.vue'
import GlobalModal from '@/components/GlobalModal.vue'

export default {
  components: { BaseButton, TheHeader, ReportModal, GlobalModal },

  data() {
    return {
      isLoading: false,
      careHistory: [], 

      reportModal: {
        visible: false,
        targetName: '',
        targetId: null
      },

      reviewForm: {
        visible: false,
        targetId: null,       
        targetSitterId: null, 
        ratings: {
          time_punctuality: 5,
          preparedness_activity: 5,
          communication_with_child: 5,
          safety_management: 5,
          communication_skill: 5
        },
        text: ''
      },

      ratingCategories: [
        { key: 'time_punctuality', label: '시간 약속:' },
        { key: 'preparedness_activity', label: '준비성:' },
        { key: 'communication_with_child', label: '교감 능력:' },
        { key: 'safety_management', label: '안전 관리:' },
        { key: 'communication_skill', label: '소통 능력:' }
      ],

      rejectModal: {
        visible: false,
        message: '',
        targetCareId: null
      }
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
        const res = await axios.get('/api/match/parent/list', {
          headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        this.careHistory = res.data;
      } catch (error) {
        console.error("내역 로드 실패:", error);
      } finally {
        this.isLoading = false;
      }
    },

    formatStatus(status) {
      const map = { 'pending': '승인 대기', 'accepted': '진행중', 'rejected': '거절됨', 'completed': '종료됨' };
      return map[status] || status;
    },
    getStatusClass(status) {
      return status; 
    },
    formatDate(dateStr) {
      return dateStr ? dateStr.split('T')[0] : '';
    },

    /* ---------- 채팅 ---------- */
    openChat(item) {
      this.$router.push(`/chat/${item.match_id}`);
    },

    /* ---------- 신고 ---------- */
    openReportModal(item) {
      this.reportModal.visible = true;
      this.reportModal.targetName = item.sitter_name; 
      this.reportModal.targetId = item.match_id;     
    },
    closeReportModal() {
      this.reportModal.visible = false;
    },

    /* ---------- 후기 ---------- */
    openReviewForm(item) {
      if (this.reviewForm.targetId === item.match_id && this.reviewForm.visible) {
        this.closeReviewForm();
        return;
      }

      this.reviewForm.visible = true;
      this.reviewForm.targetId = item.match_id;
      this.reviewForm.targetSitterId = item.sitter_id;

      // 이미 작성된 후기가 있다면 채워넣기 (API 응답 구조에 따라 조정 필요)
      if (item.has_review && item.saved_review) {
        this.reviewForm.ratings = { ...item.saved_review.ratings };
        this.reviewForm.text = item.saved_review.comment;
      } else {
        this.reviewForm.ratings = {
          time_punctuality: 5,
          preparedness_activity: 5,
          communication_with_child: 5,
          safety_management: 5,
          communication_skill: 5
        };
        this.reviewForm.text = '';
      }
    },

    closeReviewForm() {
      this.reviewForm.visible = false;
      this.reviewForm.targetId = null;
    },

    setDetailedRating(key, value) {
      this.reviewForm.ratings[key] = value;
    },

    async submitReview() {
      if (!this.reviewForm.text.trim()) {
        alert("후기 내용을 입력해주세요.");
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const payload = {
          match_id: this.reviewForm.targetId,       
          sitter_id: this.reviewForm.targetSitterId, 
          time_punctuality: this.reviewForm.ratings.time_punctuality,
          preparedness_activity: this.reviewForm.ratings.preparedness_activity,
          communication_with_child: this.reviewForm.ratings.communication_with_child,
          safety_management: this.reviewForm.ratings.safety_management,
          communication_skill: this.reviewForm.ratings.communication_skill,
          comment: this.reviewForm.text
        };

        await axios.post('/api/review/', payload, {
          headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });

        alert('후기가 성공적으로 등록되었습니다!');
        
        await this.fetchHistory(); 
        this.closeReviewForm();    

      } catch (error) {
        console.error(error);
        alert('후기 등록 실패: ' + (error.response?.data?.detail || '오류가 발생했습니다.'));
      }
    },

    /* ---------- 거절 팝업 (필요 시 구현) ---------- */
    closeRejectModal() {
      this.rejectModal.visible = false;
    },
    confirmRejectModal() {
      this.closeRejectModal();
    }
  }
}
</script>

<style scoped>
.history-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}
.history-container {
  max-width: 800px;
  margin: 30px auto;
  padding: 20px;
}
.care-item {
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
}
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-chat {
  background: none;
  border: none;
  color: #F59E0B;
  font-weight: bold;
  cursor: pointer;
}
.btn-chat:hover {
  text-decoration: underline;
}
</style>
