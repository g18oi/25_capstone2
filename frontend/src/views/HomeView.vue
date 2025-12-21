<template>
  <div class="home-page">
    <TheHeader />

    <main class="main-container">
      <section class="search-section">
        <div class="search-bar" @click="$router.push('/search')">
          <input type="text" placeholder="어떤 돌봄을 찾으시나요?" readonly>
        </div>
      </section>

      <div class="content-grid">
        <section class="main-content-section">
          
          <div v-if="!isLoggedIn">
            <h2>맞춤 돌봄 선생님을 추천해드려요 ✨</h2>
            <div class="recommendation-grid">
              <div v-for="teacher in recommendedTeachers" :key="teacher.id" class="teacher-card" @click="$router.push('/teacher/'+teacher.id)">
                <div class="teacher-photo"></div>
                <div class="teacher-info">
                  <p class="name">{{ teacher.name }}</p>
                  <p class="tags">{{ teacher.tags }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else>
            <div class="section-header-row">
              <h2>📋 내 돌봄 신청 현황</h2>
              <button class="view-history-link" @click="$router.push('/history')">
                전체 내역 보기 >
              </button>
            </div>
            
            <div v-if="myMatches.length === 0" class="empty-state">
              <p>신청한 돌봄 내역이 없습니다.</p>
              <button class="apply-btn" @click="$router.push('/search')">선생님 찾으러 가기</button>
            </div>

            <div class="match-list" v-else>
              <div v-for="match in myMatches" :key="match.match_id" class="match-card">
                <div class="match-header">
                  <span class="status-badge" :class="getStatusClass(match.status_tag)">
                    {{ match.status_tag }}
                  </span>
                  <span class="date">{{ match.date_info }}</span>
                </div>
                <div class="match-body">
                  <h3>{{ match.sitter_name }}</h3>
                  <p>{{ match.status_description }}</p>
                </div>
                <button v-if="match.show_review_button" class="action-btn">후기 작성</button>
              </div>
            </div>
          </div>

        </section>

        <aside class="sidebar-section">
          
          <div class="login-block" v-if="!isLoggedIn">
            <p>로그인하고<br>맞춤 정보를 확인하세요!</p>
            <BaseButton type="primary" @click="$router.push('/login')">로그인 / 회원가입</BaseButton>
          </div>

          <div class="user-info-block" v-else>
            <p class="welcome-msg">
              반가워요, <strong>{{ userName }}</strong>님! 👋
            </p>
            <div class="user-actions">
              <BaseButton type="primary" @click="$router.push('/history')">📋 내 돌봄 내역</BaseButton>
              <BaseButton type="secondary" @click="$router.push('/procareapply')">📝 돌봄 공고 올리기</BaseButton>
              <BaseButton type="outline" @click="$router.push('/profile/edit/parent')">⚙️ 내 정보 수정</BaseButton>
              <button class="logout-link" @click="logout">로그아웃</button>
            </div>
          </div>
          <div class="ad-block"><span>광고</span></div>
        </aside>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import BaseButton from '../components/BaseButton.vue'
import TheHeader from '../components/TheHeader.vue'

export default {
  components: { BaseButton, TheHeader },
  data() {
    return {
      isLoggedIn: false,
      userName: sessionStorage.getItem('userName') || '학부모',
      myMatches: [], 
      recommendedTeachers: [
        { id: 1, name: '김선생님', tags: '#실내놀이 #영어' },
        { id: 2, name: '이선생님', tags: '#등하원 #책읽기' },
        { id: 3, name: '박선생님', tags: '#학습지도 #한글' }
      ]
    }
  },
  async mounted() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    
    if (token) {
      this.isLoggedIn = true;
      
      try {
        const userRes = await axios.get('/api/user/me', {
           headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        if(userRes.data.name) {
          this.userName = userRes.data.name;
          sessionStorage.setItem('userName', this.userName);
        }
      } catch (e) {
        console.warn("내 정보 로드 실패(api/user/me 없음 추정), 기본값 사용");
      }

      this.fetchMyMatches(token);

    } else {
      this.isLoggedIn = false;
    }
  },
  methods: {
    async fetchMyMatches(token) {
      try {
        const res = await axios.get('/api/match/parent/list', {
          headers: { 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': 'true' }
        });
        console.log("학부모 매칭 내역:", res.data);
        this.myMatches = res.data;
      } catch (error) {
        console.error("매칭 내역 로드 실패:", error);
      }
    },
    logout() {
        localStorage.removeItem('token');
        sessionStorage.clear();
        this.isLoggedIn = false;
        this.$router.push('/login');
    },
    getStatusClass(status) {
      if (status === '진행중') return 'ongoing';
      if (status === '종료됨') return 'done';
      return 'pending';
    }
  }
}
</script>

<style scoped>
.home-page { background-color: #f8f9fa; min-height: 100vh; }
.main-container { max-width: 1200px; margin: 0 auto; padding: 0 20px 60px 20px; }

.search-section { padding: 40px 0; text-align: center; }
.search-bar { max-width: 600px; margin: 0 auto; background: white; border-radius: 50px; padding: 15px 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); cursor: pointer; display: flex; align-items: center; border: 1px solid #eee; }
.search-bar input { width: 100%; border: none; font-size: 16px; outline: none; cursor: pointer; }

.content-grid { display: flex; gap: 30px; align-items: flex-start; }
.main-content-section { flex: 3; }
.sidebar-section { flex: 1; min-width: 300px; position: sticky; top: 20px; }

.login-block, .user-info-block, .ad-block { background: white; border-radius: 20px; padding: 30px 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; border: 1px solid #f1f3f5; }
.ad-block { height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; color: #adb5bd; font-weight: bold; }

.welcome-msg { font-size: 1.1rem; margin-bottom: 20px; color: #333; }
.welcome-msg strong { color: #F59E0B; }
.user-actions { display: flex; flex-direction: column; gap: 10px; }
.logout-link { background: none; border: none; color: #adb5bd; text-decoration: underline; cursor: pointer; margin-top: 15px; font-size: 0.85rem; }

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.section-header-row h2 {
  margin: 0;
  font-size: 1.4rem;
}
.view-history-link {
  background: none;
  border: none;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
  font-weight: 600;
}
.view-history-link:hover {
  color: #F59E0B;
  text-decoration: underline;
}

.recommendation-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
.teacher-card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); cursor: pointer; transition: transform 0.2s; }
.teacher-card:hover { transform: translateY(-5px); }
.teacher-photo { height: 150px; background-color: #eee; }
.teacher-info { padding: 15px; }
.teacher-info .name { font-weight: bold; font-size: 1.1rem; margin: 0 0 5px 0; }
.teacher-info .tags { font-size: 0.85rem; color: #666; }

.match-list { display: flex; flex-direction: column; gap: 15px; }
.match-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid transparent; }
.match-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.status-badge { padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; }
.status-badge.pending { background: #E3F2FD; color: #1976D2; }
.status-badge.ongoing { background: #E8F5E9; color: #2E7D32; }
.status-badge.done { background: #eee; color: #666; }
.date { font-size: 0.9rem; color: #888; }
.match-body h3 { margin: 0 0 5px 0; font-size: 1.1rem; color: #333; }
.match-body p { margin: 0; color: #666; font-size: 0.95rem; }
.action-btn { margin-top: 15px; padding: 8px 15px; background: #FFF3E0; color: #F57C00; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }

.empty-state { background: white; padding: 40px; border-radius: 15px; text-align: center; color: #888; }
.apply-btn { margin-top: 15px; padding: 10px 20px; background: #FBBF24; color: white; border: none; border-radius: 20px; font-weight: bold; cursor: pointer; }

@media (max-width: 900px) {
  .content-grid { flex-direction: column; }
  .main-content-section, .sidebar-section { width: 100%; }
  .sidebar-section { order: -1; margin-bottom: 20px; }
}
</style>