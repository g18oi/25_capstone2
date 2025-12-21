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
import BaseButton from '../components/BaseButton.vue';
import TheHeader from '../components/TheHeader.vue';

export default {
  emits: ['show-modal'],
  components: {
    BaseButton,
    TheHeader
  },
  data() {
    return {
      selectedFile: null,
      fileName: ''
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.selectedFile = file;
      this.fileName = file.name;
    },
    submitDocuments() {
      if (!this.selectedFile) {
      
        alert('파일을 먼저 선택해주세요.');
        return;
      }
      console.log('서버로 제출할 파일:', this.selectedFile);
      alert('증명서가 성공적으로 제출되었습니다. 관리자 확인 후 활동이 가능합니다.');
      this.$router.push('/teacher-home');
    },
    

    skipOnboarding() {
      if (confirm('자격 증명을 나중에 하시겠습니까?\n인증되지 않은 상태에서는 일부 활동이 제한될 수 있습니다.')) {
        this.$router.push('/teacher-home');
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
.file-upload-area { border: 2px dashed #4CAF50; border-radius: 12px; padding: 40px 20px; margin-bottom: 30px; cursor: pointer; transition: background-color 0.2s; }
.file-upload-area:hover { background-color: #f1f8e9; }
.upload-icon { font-size: 40px; margin-bottom: 15px; }
.upload-text { font-size: 18px; font-weight: 600; color: #333; }
.upload-hint { font-size: 14px; color: #888; margin-top: 8px; }
.file-info { text-align: center; }
.file-name-icon { font-size: 30px; color: #4CAF50; }
.file-name { font-size: 16px; font-weight: 600; color: #333; margin: 10px 0; word-break: break-all; }
.file-change-hint { font-size: 13px; color: #aaa; }


.skip-area {
  margin-top: 20px;
}
.skip-btn {
  background: none;
  border: none;
  color: #868e96;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s;
}
.skip-btn:hover {
  color: #495057;
}
</style>