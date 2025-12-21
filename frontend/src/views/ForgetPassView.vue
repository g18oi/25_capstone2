<template>
  <div>
    <TheHeader />
    <main class="auth-layout">
      <div class="login-card">
        <div class="logo">
          <span class="logo-icon">📧</span>
          <span class="logo-text">비밀번호 찾기</span>
        </div>
        <p class="tagline">
          가입한 이메일을 입력해주시면<br>
          비밀번호 재설정 링크를 보내드립니다.
        </p>

        <form @submit.prevent="requestResetLink">
          <div class="input-group">
            <label for="email">이메일 주소</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="example@email.com" 
              required
              :disabled="isLoading"
            >
          </div>

          <BaseButton type="primary" :disabled="isLoading">
            {{ isLoading ? '전송 중...' : '재설정 링크 발송' }}
          </BaseButton>
          
          <p v-if="message" :class="['message-text', isError ? 'error' : 'success']">
            {{ message }}
          </p>
        </form>
        
        <div class="footer-links">
          <router-link to="/login" class="footer-text">로그인으로 돌아가기</router-link>
        </div>
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
      email: '',
      message: '',
      isError: false,
      isLoading: false
    };
  },
  methods: {
    async requestResetLink() {
      if (!this.email) return;

      this.isLoading = true;
      this.message = '';
      
      try {
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.message = '이메일로 비밀번호 재설정 링크가 발송되었습니다. 메일함을 확인해주세요.';
        this.isError = false;
      } catch (error) {
        this.message = '오류가 발생했습니다. 다시 시도해주세요.';
        this.isError = true;
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

.input-group { text-align: left; margin-bottom: 25px; }
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


.message-text {
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.4;
}
.message-text.success {
  background-color: #E8F5E9;
  color: #2E7D32;
}
.message-text.error {
  background-color: #FFEBEE;
  color: #C62828;
}

.footer-links { margin-top: 30px; }
.footer-text { font-size: 14px; color: #888; text-decoration: none; }
.footer-text:hover { color: #FBBF24; text-decoration: underline; }
</style>