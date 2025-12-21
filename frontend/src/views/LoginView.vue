<template>
  <div class="page-container">
    <TheHeader />
    <main class="auth-layout">
      <div class="login-card">
        <div class="logo-area">
          <span class="logo-icon">🔗</span>
          <span class="logo-text">아이Link</span>
        </div>
        <p class="tagline">아이와 세상을 연결하는 다리</p>

        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">이메일 (아이디)</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="example@email.com" 
              required 
            />
          </div>

          <div class="input-group">
            <label for="password">비밀번호</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="비밀번호를 입력하세요" 
              required 
            />
          </div>

          <button type="submit" class="login-btn">
            로그인
          </button>
        </form>

        <div class="link-actions">
          <span class="link-item" @click="$router.push('/signup')">회원가입</span>
          <span class="divider">|</span>
          <span class="link-item" @click="$router.push('/forgot-password')">비밀번호 찾기</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { TheHeader },
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      if (!this.email || !this.password) {
        alert('이메일과 비밀번호를 입력해주세요.');
        return;
      }

      try {
        const formData = new FormData();
        formData.append('username', this.email);
        formData.append('password', this.password);

        const response = await axios.post('/api/auth/token', formData, {
          headers: { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'ngrok-skip-browser-warning': 'true'
          }
        });


        const { access_token, role, name } = response.data;


        localStorage.setItem('token', access_token);
        sessionStorage.setItem('token', access_token);
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('userRole', role);
        sessionStorage.setItem('userName', name || (role === 'sitter' ? '선생님' : '학부모'));

        console.log("로그인 성공! 역할:", role);

        if (role === 'sitter') {
          this.$router.push('/teacher-home');
        } else {
          this.$router.push('/home'); // 학부모는 home으로
        }

      } catch (error) {
        console.error('로그인 에러:', error);
        alert('로그인 실패: 아이디 또는 비밀번호를 확인해주세요.');
      }
    }
  }
};
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
}

.auth-layout {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.logo-area {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.logo-icon {
  font-size: 32px;
  margin-right: 8px;
}

.logo-text {
  font-size: 28px;
  font-weight: 800;
  color: #333;
}

.tagline {
  color: #666;
  margin-bottom: 30px;
  font-size: 15px;
}

.input-group {
  text-align: left;
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #444;
  margin-bottom: 8px;
}

.input-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 15px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.input-group input:focus {
  outline: none;
  border-color: #FBBF24;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background-color: #FBBF24;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s;
}

.login-btn:hover {
  background-color: #F59E0B;
}

.link-actions {
  margin-top: 25px;
  font-size: 14px;
  color: #888;
}

.link-item {
  cursor: pointer;
  transition: color 0.2s;
}

.link-item:hover {
  color: #333;
  text-decoration: underline;
}

.divider {
  margin: 0 10px;
  color: #ddd;
}
</style>