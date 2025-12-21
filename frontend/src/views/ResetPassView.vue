<template>
  <div>
    <TheHeader />
    <main class="auth-layout">
      <div class="login-card">
        <div class="logo">
          <span class="logo-icon">🔐</span>
          <span class="logo-text">비밀번호 변경</span>
        </div>
        <p class="tagline">새로운 비밀번호를 입력해주세요.</p>

        <form @submit.prevent="resetPassword">
          <div class="input-group">
            <label for="newPassword">새 비밀번호</label>
            <input 
              type="password" 
              id="newPassword" 
              v-model="newPassword" 
              placeholder="새 비밀번호 입력" 
              required
            >
          </div>
          <div class="input-group">
            <label for="confirmPassword">비밀번호 확인</label>
            <input 
              type="password" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              placeholder="새 비밀번호 다시 입력" 
              required
            >
            <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
          </div>

          <BaseButton type="primary" :disabled="isLoading">
            {{ isLoading ? '변경 중...' : '비밀번호 변경하기' }}
          </BaseButton>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue';
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { BaseButton, TheHeader },
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      token: '',
      errorMessage: '',
      isLoading: false
    };
  },
  created() {
    this.token = this.$route.query.token;
    
    if (!this.token) {
      alert('유효하지 않은 접근입니다.');
      this.$router.push('/login');
    }
  },
  methods: {
    async resetPassword() {
      if (this.newPassword.length < 6) {
        this.errorMessage = '비밀번호는 6자 이상이어야 합니다.';
        return;
      }
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = '비밀번호가 서로 일치하지 않습니다.';
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';

      try {
    
        await new Promise(resolve => setTimeout(resolve, 1000));

        alert('비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.');
        this.$router.push('/login');

      } catch (error) {
        this.errorMessage = '토큰이 만료되었거나 오류가 발생했습니다.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>

.auth-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  min-height: calc(100vh - 75px);
  background-color: #f8f9fa;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}


.logo { display: flex; justify-content: center; align-items: center; margin-bottom: 25px; }
.logo-icon { font-size: 38px; margin-right: 10px; }
.logo-text { font-size: 32px; font-weight: 800; color: #333; }
.tagline { font-size: 16px; color: #666; margin-bottom: 30px; line-height: 1.5; }


.input-group { text-align: left; margin-bottom: 20px; }
.input-group label { display: block; font-size: 14px; color: #555; margin-bottom: 8px; font-weight: 600; }
.input-group input { 
  width: 100%; 
  padding: 14px; 
  border: 1px solid #e0e0e0; 
  border-radius: 10px; 
  font-size: 16px; 
  box-sizing: border-box; 
  transition: all 0.2s; 
}
.input-group input:focus { 
  outline: none; 
  border-color: #FBBF24; 
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.2); 
}

.error-text {
  color: #e53935;
  font-size: 13px;
  margin-top: 8px;
}
</style>