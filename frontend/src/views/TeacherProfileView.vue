<template>
  <div class="profile-page">
    <TheHeader />

    <div v-if="isLoading" class="loading-screen">선생님 정보 불러오는 중...</div>

    <main v-else class="profile-container">
      
      <section class="profile-header-card">
        <div class="profile-image-wrapper">
          <div class="profile-placeholder">👩‍🏫</div>
        </div>
        <div class="profile-summary">
          <div class="name-row">
            <h1 class="name">{{ teacher.name }} 선생님</h1>
            <span class="badge">인증 완료 ✅</span>
          </div>
          <p class="one-liner">"{{ teacher.oneLiner || '한 줄 소개가 없습니다.' }}"</p>
          <div class="tags-row">
            <span v-for="tag in teacher.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </section>

      <section class="info-grid">
        <div class="info-card">
          <h3>기본 정보</h3>
          <ul class="info-list">
            <li><span class="label">나이</span><span class="value">{{ teacher.age }}세 (예상)</span></li>
            <li><span class="label">성별</span><span class="value">{{ teacher.gender }}</span></li>
            <li><span class="label">거주지</span><span class="value">{{ teacher.location }}</span></li>
          </ul>
        </div>

        <div class="info-card">
          <h3>활동 조건</h3>
          <ul class="info-list">
            <li><span class="label">희망 시급</span><span class="value highlight">{{ formatPay(teacher.wage) }}원</span></li>
            <li><span class="label">정산 방식</span><span class="value">{{ teacher.availableDays }}</span></li>
            <li><span class="label">CCTV 동의</span><span class="value">{{ teacher.cctv ? '가능 ⭕' : '불가능 ❌' }}</span></li>
          </ul>
        </div>
      </section>

      <section class="intro-section card-style">
        <h3>선생님 소개</h3>
        <p class="intro-text">{{ teacher.introduction }}</p>
      </section>

      <ReviewStats 
        :stats="reviewStats" 
        :rematchProbability="rematchProbability"
      />

    </main>

    <div class="bottom-action-bar" v-if="!isLoading">
      <BaseButton type="primary" class="match-btn full-width" @click="requestMatching">
        매칭 신청하기
      </BaseButton>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import BaseButton from '@/components/BaseButton.vue'
import TheHeader from '@/components/TheHeader.vue'
import ReviewStats from '@/components/ReviewStats.vue' 

export default {
  components: { BaseButton, TheHeader, ReviewStats }, 
  data() {
    return {
      isLoading: true,
      teacher: {
        id: null,
        name: '',
        age: 0,
        gender: '',
        location: '',
        oneLiner: '',
        tags: [],
        wage: 0,
        availableDays: '',
        cctv: false,
        introduction: ''
      },
      reviewStats: {
        avg_time_punctuality: 0,
        avg_preparedness_activity: 0,
        avg_communication_with_child: 0,
        avg_safety_management: 0,
        avg_communication_skill: 0
      },
      rematchProbability: null
    }
  },
  mounted() {
    const id = this.$route.params.id;
    this.fetchTeacherProfile(id);
  },
  methods: {
    async fetchTeacherProfile(id) {
        try {
            const res = await axios.get(`/api/search/sitter/${id}`, {
                 headers: { 'ngrok-skip-browser-warning': 'true' }
            });
            
            this.teacher = res.data;
            
            if (res.data.reviewStats) {
                this.reviewStats = res.data.reviewStats;
            }
            this.rematchProbability = res.data.rematchProbability;

        } catch (error) {
            console.error("프로필 로드 실패:", error);
            alert("선생님 정보를 불러올 수 없습니다.");
            this.$router.go(-1);
        } finally {
            this.isLoading = false;
        }
    },
    formatPay(pay) {
        return pay ? Number(pay).toLocaleString() : '0';
    },

    async requestMatching() {
      if(!confirm(`${this.teacher.name} 선생님에게 매칭을 신청하시겠습니까?`)) return;
      
      try {
        const token = localStorage.getItem('token');
        if(!token) {
            alert("로그인이 필요합니다.");
            this.$router.push('/login');
            return;
        }
        
        const userRes = await axios.get('/api/user/me', {
           headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        const parentId = userRes.data.id;

        await axios.post('/api/match/request', null, {
            params: { parent_id: parentId, sitter_id: this.teacher.id },
            headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });

  
        alert('매칭 신청이 완료되었습니다!\n선생님이 수락하면 채팅방이 생성됩니다.');
        this.$router.push('/history');

      } catch (error) {
         console.error(error);
         alert(error.response?.data?.detail || "매칭 신청 중 오류가 발생했습니다.");
      }
    }

  }
}
</script>

<style scoped>
/* 기존 스타일 유지 */
.loading-screen { text-align: center; padding: 50px; font-weight: bold; color: #888; }
.profile-page { background: #f8f9fa; min-height: 100vh; padding-bottom: 80px; }
.profile-container { max-width: 800px; margin: 0 auto; padding: 20px; }

.profile-header-card { background: white; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.profile-placeholder { font-size: 60px; background: #eee; width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; }
.name { font-size: 1.5rem; font-weight: 800; margin: 0; display: inline-block; margin-right: 8px; }
.badge { background: #E8F5E9; color: #2E7D32; padding: 4px 8px; border-radius: 10px; font-size: 0.8rem; font-weight: bold; vertical-align: middle; }
.one-liner { color: #555; margin: 10px 0 15px; font-style: italic; }
.tags-row { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.tag { background: #f1f3f5; color: #495057; padding: 5px 12px; border-radius: 20px; font-size: 0.9rem; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.info-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.info-card h3 { margin: 0 0 15px 0; font-size: 1.1rem; border-bottom: 2px solid #FBBF24; display: inline-block; padding-bottom: 5px; }
.info-list { list-style: none; padding: 0; margin: 0; }
.info-list li { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 0.95rem; }
.info-list .label { color: #888; }
.info-list .value { font-weight: bold; color: #333; }
.value.highlight { color: #F59E0B; font-size: 1.1rem; }

.card-style { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
.intro-text { line-height: 1.6; color: #444; white-space: pre-line; }

.bottom-action-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 15px; display: flex; justify-content: center; gap: 10px; box-shadow: 0 -5px 20px rgba(0,0,0,0.05); z-index: 100; }

.match-btn.full-width { width: 100% !important; margin-top: 0 !important; max-width: 600px; }

@media (max-width: 600px) {
  .info-grid { grid-template-columns: 1fr; }
}
</style>