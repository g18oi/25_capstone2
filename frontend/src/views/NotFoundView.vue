<template>
  <div class="not-found">
    <div class="icon">🤔</div>
    <h1>길을 잃으셨나요?</h1>
    <p>요청하신 페이지를 찾을 수 없습니다.</p>
    <button @click="goHome" class="home-btn">홈으로 돌아가기</button>
  </div>
</template>

<script>
export default {
  methods: {
    goHome() {
      // 로그인한 유저의 역할(role)을 확인합니다.
      const userRole = sessionStorage.getItem('userRole');

      if (userRole === 'sitter') {
        this.$router.push('/teacher-home'); // 선생님이면 선생님 홈으로
      } else {
        this.$router.push('/'); // 그 외엔 기본 홈(학부모 홈)으로
      }
    }
  }
}
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  background-color: #f8f9fa;
}
.icon { font-size: 60px; margin-bottom: 20px; }
h1 { font-size: 24px; color: #333; margin-bottom: 10px; }
p { color: #666; margin-bottom: 30px; }
.home-btn {
  background-color: #FBBF24;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: bold;
  cursor: pointer;
  font-size: 16px;
}
.home-btn:hover { background-color: #F59E0B; }
</style>