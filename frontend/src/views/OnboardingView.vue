<template>
  <div>
    <TheHeader />
    <main class="auth-layout">
      <div class="onboarding-card">
        <div class="logo">
          <span class="logo-icon">📄</span>
          <span class="logo-text">자격 증명</span>
        </div>
        <p class="tagline">
          신뢰할 수 있는 서비스를 위해<br>자격 증명서를 제출해주세요.
        </p>
        
        <div class="file-upload-area" @click="triggerFileInput">
          <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" accept="image/*,.pdf">
          <div v-if="!fileName">
            <p class="upload-icon">⬆️</p>
            <p class="upload-text">클릭하여 파일 선택</p>
            <p class="upload-hint">(이미지 또는 PDF 파일)</p>
          </div>
          <div v-else class="file-info">
            <p class="file-name-icon">✅</p>
            <p class="file-name">{{ fileName }}</p>
            <p class="file-change-hint">파일을 변경하려면 다시 클릭하세요.</p>
          </div>
        </div>

        <BaseButton @click="submitDocuments" type="secondary">제출하고 시작하기</BaseButton>

        <div class="skip-area">
          <button class="skip-btn" @click="skipOnboarding">다음에 설정하기 ></button>
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
      file: null,
      fileName: ''
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.file = file;
        this.fileName = file.name;
      }
    },
    async submitDocuments() {
      if (!this.file) {
        alert('파일을 선택해주세요.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        await axios.post('/api/certificate/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${token}`,
            'ngrok-skip-browser-warning': 'true'
          }
        });

        alert('제출이 완료되었습니다! 관리자 심사 후 인증됩니다.');
        this.$router.push('/teacher-home');

      } catch (error) {
        console.error('업로드 실패:', error);
        alert('업로드 중 오류가 발생했습니다.');
      }
    },
    skipOnboarding() {
      if(confirm('자격 증명을 건너뛰면 활동에 제약이 있을 수 있습니다. 계속하시겠습니까?')) {
        this.$router.push('/teacher-home');
      }
    }
  }
};
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

.onboarding-card {
  width: 100%;
  max-width: 480px;
  padding: 40px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.logo { display: flex; justify-content: center; align-items: center; margin-bottom: 15px; }
.logo-icon { font-size: 38px; margin-right: 10px; }
.logo-text { font-size: 36px; font-weight: 800; color: #333; }
.tagline { font-size: 18px; color: #666; margin-bottom: 40px; line-height: 1.6; }

.file-upload-area { 
  border: 2px dashed #4CAF50; 
  border-radius: 12px; padding: 40px 20px; margin-bottom: 30px; 
  cursor: pointer; transition: background-color 0.2s; 
}
.file-upload-area:hover { background-color: #f1f8e9; }

.upload-icon { font-size: 40px; margin-bottom: 10px; }
.upload-text { font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 5px; }
.upload-hint { font-size: 14px; color: #999; }

.file-info { display: flex; flex-direction: column; align-items: center; }
.file-name-icon { font-size: 30px; margin-bottom: 10px; }
.file-name { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 5px; }
.file-change-hint { font-size: 13px; color: #888; }

/* [추가] 선생님 테마(녹색) 버튼 스타일 */
.submit-btn {
  width: 100%;
  padding: 15px;
  background-color: #4CAF50; /* 선생님 테마 녹색 */
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
}

.submit-btn:hover {
  background-color: #43A047;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  box-shadow: none;
}

.skip-area { margin-top: 20px; }
.skip-btn {
  background: none;
  border: none;
  color: #999;
  text-decoration: underline;
  cursor: pointer;
  font-size: 14px;
}
.skip-btn:hover { color: #666; }
</style>