<template>
  <div class="home-page">
    <TheHeader />

    <main class="main-container">
      <div class="content-grid">
        
        <section class="main-content-section">
          
          <div class="section-block" v-if="ongoingMatches.length > 0">
            <div class="section-header-row">
              <h2>🔥 진행 중인 돌봄</h2>
            </div>
            
            <div class="card-list">
              <div 
                v-for="match in ongoingMatches" 
                :key="match.match_id" 
                class="request-card ongoing-card"
                @click="goToChat(match.match_id)"
              >
                <div class="card-header">
                  <span class="badge ongoing">진행중</span>
                  <span class="date">{{ formatDate(match.created_at) }} 시작</span>
                </div>
                <div class="card-body">
                  <h3>{{ match.parent_name }} 학부모님</h3>
                  <div class="info-row">
                    <span class="icon">📍</span>
                    <span>{{ match.location || '위치 정보 없음' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="icon">💬</span>
                    <span class="chat-link">채팅방 바로가기 ></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="section-block">
            <div class="section-header-row">
              <h2>📋 들어온 돌봄 요청 (대기중)</h2>
              <button class="view-history-link" @click="$router.push('/teacher/history')">
                전체보기 >
              </button>
            </div>
            
            <div v-if="isLoading" class="loading-state">
               <p>데이터를 불러오는 중입니다...</p>
            </div>
            <div v-else-if="requests.length === 0" class="empty-state">
               <p>현재 대기 중인 요청이 없습니다.</p>
            </div>
            
            <div v-else class="card-list">
              <div 
                v-for="req in requests" 
                :key="req.match_id" 
                class="request-card"
                @click="goToDetail(req.match_id)"
              >
                <div class="card-header">
                  <span class="badge new">NEW</span>
                  <span class="date">{{ formatDate(req.created_at) }}</span>
                </div>
                <div class="card-body">
                  <h3>{{ req.parent_name }}</h3>
                  <div class="info-row">
                    <span class="icon">📍</span>
                    <span>{{ req.location || '지역 정보 없음' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="icon">💰</span>
                    <span class="highlight">{{ formatPay(req.hourly_pay) }}원</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </section>

        <aside class="sidebar-section">
          <div class="sidebar-card user-info-block">
            <p class="welcome-msg">
              안녕하세요,<br><strong>{{ userName }} 선생님!</strong> 👩‍🏫
            </p>

            <div class="certification-status">
              <button v-if="!isVerified && !hasCertificate" class="action-btn primary" @click="$router.push('/onboarding')">
                📄 자격 증명 제출하기
              </button>
              
              <button v-else-if="!isVerified && hasCertificate" class="action-btn pending" disabled>
                ⏳ 심사 대기 중입니다
              </button>
              
              <button v-else class="action-btn verified" disabled>
                ✅ 인증된 선생님입니다
              </button>
            </div>

            <div class="menu-links">
              <button class="menu-btn" @click="$router.push('/teacher/history')">
                📨 내 돌봄 내역 관리
              </button>
              <button class="menu-btn" @click="$router.push('/profile/edit/teacher')">
                ⚙️ 프로필 수정
              </button>
            </div>
          </div>

          <div class="sidebar-card ad-block">
            <span>광고 영역</span>
          </div>
        </aside>

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
      isLoading: false,
      userName: sessionStorage.getItem('userName') || '선생님',
      isVerified: false,     
      hasCertificate: false, 
      requests: [],          
      ongoingMatches: []     
    };
  },
  async mounted() {
    await this.fetchUserInfo(); 
    await this.fetchRequests(); 
  },
  methods: {
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('token');
        if (!token) return;

        const res = await axios.get('/api/user/me', {
           headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        
        const user = res.data;
        this.userName = user.name;
      
        if (user.certifications && user.certifications.length > 0) {
            this.hasCertificate = true;
            this.isVerified = true; 
        }

      } catch (e) {
        console.warn("유저 정보 로드 실패", e);
      }
    },
    async fetchRequests() {
      this.isLoading = true;
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/match/sitter/list', {
          headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        
        const allMatches = res.data;
        // 상태별 분리
        this.requests = allMatches.filter(m => m.status === 'pending');
        this.ongoingMatches = allMatches.filter(m => m.status === 'accepted');

      } catch (error) {
        console.error("매칭 데이터 로드 실패:", error);
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      return dateStr.split('T')[0];
    },
    formatPay(pay) {
      return pay ? Number(pay).toLocaleString() : '0';
    },
    goToDetail(id) {
      this.$router.push(`/teacher/request/${id}`);
    },
    goToChat(id) {
      this.$router.push(`/chat/${id}`);
    }
  }
};
</script>

<style scoped>
/* 전체 레이아웃 */
.home-page { background-color: #f8f9fa; min-height: 100vh; }
.main-container { max-width: 1200px; margin: 0 auto; padding: 20px; }

/* 그리드 레이아웃 (왼쪽 3 : 오른쪽 1) */
.content-grid { display: flex; gap: 30px; align-items: flex-start; }
.main-content-section { flex: 3; }
.sidebar-section { flex: 1; min-width: 280px; position: sticky; top: 20px; }

/* 섹션 스타일 */
.section-block { margin-bottom: 40px; }
.section-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.section-header-row h2 { font-size: 1.3rem; color: #333; margin: 0; font-weight: 800; }
.view-history-link { background: none; border: none; color: #888; cursor: pointer; font-size: 0.9rem; }

/* 카드 리스트 */
.card-list { display: flex; flex-direction: column; gap: 15px; }

/* 기본 카드 스타일 */
.request-card { 
  background: white; border-radius: 15px; padding: 20px; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.05); cursor: pointer; 
  transition: transform 0.2s, border-color 0.2s; border: 1px solid transparent; 
}
.request-card:hover { transform: translateY(-3px); border-color: #FBBF24; }

/* 진행 중인 카드 (강조) */
.ongoing-card { border: 1px solid #4CAF50; background-color: #F1F8E9; }
.ongoing-card:hover { border-color: #2E7D32; background-color: #E8F5E9; }

.card-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.badge { font-size: 0.8rem; padding: 4px 8px; border-radius: 10px; font-weight: bold; }
.badge.new { background-color: #FFF3E0; color: #F57C00; }
.badge.ongoing { background-color: #C8E6C9; color: #2E7D32; }
.date { font-size: 0.85rem; color: #999; }

.card-body h3 { margin: 0 0 10px 0; font-size: 1.1rem; color: #333; }
.info-row { display: flex; align-items: center; gap: 8px; color: #666; font-size: 0.95rem; margin-bottom: 4px; }
.highlight { color: #F59E0B; font-weight: bold; }
.chat-link { color: #2E7D32; font-weight: bold; font-size: 0.9rem; }

/* 사이드바 스타일 */
.sidebar-card { 
  background: white; border-radius: 20px; padding: 30px 25px; 
  box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; border: 1px solid #f1f3f5; 
}
.welcome-msg { font-size: 1.1rem; margin-bottom: 25px; color: #333; line-height: 1.5; }
.welcome-msg strong { color: #4CAF50; font-size: 1.3rem; }

.certification-status { margin-bottom: 20px; }
.action-btn { 
  width: 100%; padding: 12px; border-radius: 10px; font-weight: bold; cursor: pointer; border: none; font-size: 0.95rem; 
}
.action-btn.primary { background-color: #4CAF50; color: white; box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3); }
.action-btn.primary:hover { background-color: #43A047; }
.action-btn.pending { background-color: #FFF3E0; color: #F57C00; cursor: default; }
.action-btn.verified { background-color: #E8F5E9; color: #2E7D32; cursor: default; border: 1px solid #C8E6C9; }

.menu-links { display: flex; flex-direction: column; gap: 10px; }
.menu-btn { 
  background: white; border: 1px solid #eee; padding: 12px; border-radius: 10px; 
  color: #555; font-weight: bold; cursor: pointer; transition: all 0.2s; 
}
.menu-btn:hover { background-color: #f8f9fa; color: #333; border-color: #ddd; }

.ad-block { height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; color: #adb5bd; font-weight: bold; }

/* 로딩/빈 상태 */
.loading-state, .empty-state { text-align: center; padding: 40px; color: #888; background: white; border-radius: 15px; }

/* 반응형 */
@media (max-width: 900px) {
  .content-grid { flex-direction: column; }
  .main-content-section, .sidebar-section { width: 100%; }
  .sidebar-section { order: -1; margin-bottom: 20px; }
}
</style>