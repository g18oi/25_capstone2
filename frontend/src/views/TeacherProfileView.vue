<template>
  <div class="profile-page">
    <TheHeader />

    <main class="profile-container">
      <section class="profile-header-card">
        <div class="profile-image-wrapper">
          <div class="profile-placeholder"></div>
        </div>
        <div class="profile-summary">
          <div class="name-row">
            <h1 class="name">{{ teacher.name }} 선생님</h1>
            <span class="badge">인증 완료 ✅</span>
          </div>
          <p class="one-liner">"{{ teacher.oneLiner }}"</p>
          <div class="tags-row">
            <span v-for="tag in teacher.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </section>

      <section class="info-grid">
        <div class="info-card">
          <h3>기본 정보</h3>
          <ul class="info-list">
            <li>
              <span class="label">나이</span>
              <span class="value">{{ teacher.age }}세</span>
            </li>
            <li>
              <span class="label">성별</span>
              <span class="value">{{ teacher.gender }}</span>
            </li>
            <li>
              <span class="label">거주지</span>
              <span class="value">{{ teacher.location }}</span>
            </li>
          </ul>
        </div>

        <div class="info-card">
          <h3>활동 조건</h3>
          <ul class="info-list">
            <li>
              <span class="label">희망 시급</span>
              <span class="value highlight">{{ teacher.wage.toLocaleString() }}원</span>
            </li>
            <li>
              <span class="label">활동 가능</span>
              <span class="value">{{ teacher.availableDays }}</span>
            </li>
            <li>
              <span class="label">CCTV 동의</span>
              <span class="value">{{ teacher.cctv ? '가능 ⭕' : '불가능 ❌' }}</span>
            </li>
          </ul>
        </div>
      </section>

      <section class="intro-section card-style">
        <h3>선생님 소개</h3>
        <p class="intro-text">
          {{ teacher.introduction }}
        </p>
      </section>

      <section class="review-section card-style">
        <div class="section-header">
          <h3>학부모 후기 ({{ teacher.reviewCount }})</h3>
          <span class="rating">⭐️ {{ teacher.rating }}</span>
        </div>
        <div class="review-preview" v-if="teacher.reviewCount > 0">
          <p>"{{ teacher.latestReview }}"</p>
        </div>
      </section>
    </main>

    <div class="bottom-action-bar">
      <div class="action-text">
        <p>이 선생님이 마음에 드시나요?</p>
        <span>매칭을 신청하면 연락처가 공유됩니다.</span>
      </div>
      <BaseButton type="primary" class="match-btn" @click="startMatching">
        매칭 신청하기
      </BaseButton>
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue';
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { BaseButton, TheHeader },
  data() {
    return {
    
      teacher: {
        id: this.$route.params.id,
        name: '김선생님',
        age: 26,
        gender: '여',
        location: '서울시 강남구',
        oneLiner: '아이와 함께하는 시간이 가장 행복한 선생님입니다!',
        tags: ['#실내놀이', '#영어', '#에너지넘침'],
        wage: 15000,
        availableDays: '월, 수, 금 (오후)',
        cctv: true,
        introduction: `안녕하세요! 유아교육과를 전공하고 있는 김선생님입니다. 
아이들의 눈높이에서 소통하며, 단순한 놀이가 아니라 배움이 있는 시간을 만들어가고 싶습니다. 
책 읽어주기와 영어 놀이에 자신 있습니다. 믿고 맡겨주시면 최선을 다하겠습니다!`,
        rating: 4.8,
        reviewCount: 12,
        latestReview: '시간 약속도 잘 지키시고 아이가 선생님 오시는 날만 기다려요^^'
      }
    };
  },
  methods: {
    startMatching() {

      if (confirm(`${this.teacher.name} 선생님에게 매칭을 신청하시겠습니까?`)) {
        alert('신청이 완료되었습니다! 내역 페이지로 이동합니다.');
        this.$router.push('/history');
      }
    }
  }
}
</script>

<style scoped>
.profile-page {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding-bottom: 100px;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px 20px;
}


.profile-header-card {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  display: flex;
  gap: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-bottom: 25px;
  align-items: center;
}

.profile-image-wrapper {
  flex-shrink: 0;
}

.profile-placeholder {
  width: 120px;
  height: 120px;
  background-color: #e9ecef;
  border-radius: 50%;
  border: 4px solid #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.profile-summary {
  flex-grow: 1;
  text-align: left;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.name {
  font-size: 26px;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.badge {
  background-color: #E8F5E9;
  color: #2E7D32;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 600;
}

.one-liner {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
}

.tags-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  background-color: #FFFBEB;
  color: #F59E0B;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #FCD34D;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

.info-card {
  background-color: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.info-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 2px solid #f1f3f5;
  padding-bottom: 10px;
  text-align: left;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
}

.info-list li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 15px;
}

.info-list .label {
  color: #868e96;
}

.info-list .value {
  font-weight: 600;
  color: #495057;
}

.info-list .value.highlight {
  color: #F59E0B;
  font-weight: 700;
}


.card-style {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  margin-bottom: 25px;
  text-align: left;
}

.card-style h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 15px;
  color: #333;
}

.intro-text {
  line-height: 1.6;
  color: #555;
  white-space: pre-line; 
}


.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.rating {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.review-preview {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  color: #666;
  font-style: italic;
}

.bottom-action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: white;
  padding: 20px;
  box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
  display: flex;
  justify-content: center; 
  align-items: center;
  gap: 20px; 
  box-sizing: border-box;
  z-index: 1000;
}

.action-text {
  text-align: left;
}

.action-text p {
  font-weight: 700;
  font-size: 16px;
  margin: 0 0 4px 0;
  color: #333;
}

.action-text span {
  font-size: 13px;
  color: #888;
}

.match-btn {
  min-width: 150px;
}

/* 모바일 대응 */
@media (max-width: 600px) {
  .profile-header-card {
    flex-direction: column;
    text-align: center;
  }
  .profile-summary {
    text-align: center;
  }
  .name-row {
    justify-content: center;
  }
  .tags-row {
    justify-content: center;
  }
  .info-grid {
    grid-template-columns: 1fr;
  }
  .bottom-action-bar {
    justify-content: space-between; 
  }
}
</style>