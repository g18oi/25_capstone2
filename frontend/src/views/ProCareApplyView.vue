<template>
  <div class="form-page-container">
    <div class="form-card">
      
      <header class="form-header primary-bg">
        <h1>돌보미 선생님 지원</h1>
        <p>ProCare와 함께 따뜻한 돌봄을 실천할<br>전문가 선생님을 모십니다.</p>
      </header>

      <form @submit.prevent="handleSubmit" class="form-body">
        
        <fieldset class="form-section">
          <legend>기본 정보</legend>
          
          <div class="form-grid">
            <div class="form-group full-width">
              <label>프로필 사진</label>
              <div class="profile-uploader">
                <img :src="profilePreview || 'https://via.placeholder.com/100'" alt="미리보기" class="profile-preview">
                <input type="file" id="profilePicture" @change="handleProfileUpload" accept="image/*">
                <label for="profilePicture" class="btn-upload">사진 변경</label>
              </div>
            </div>

            <div class="form-group">
              <label for="name">이름</label>
              <input type="text" id="name" v-model="formData.name" required placeholder="홍길동">
            </div>

            <div class="form-group">
              <label for="birthdate">생년월일</label>
              <input type="date" id="birthdate" v-model="formData.birthdate" required>
            </div>

            <div class="form-group">
              <label for="contact">연락처</label>
              <input type="tel" id="contact" v-model="formData.contact" required placeholder="010-0000-0000">
            </div>

            <div class="form-group">
              <label for="email">이메일</label>
              <input type="email" id="email" v-model="formData.email" required placeholder="example@email.com">
            </div>

            <div class="form-group full-width">
              <label for="address">주소</label>
              <input type="text" id="address" v-model="formData.address" required placeholder="상세 주소">
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>전문성 정보</legend>

          <div class="form-group">
            <label for="introduction">한 줄 자기소개</label>
            <input type="text" id="introduction" v-model="formData.introduction" placeholder="예: 10년 경력의 영유아 전문 보육교사입니다.">
          </div>

          <div class="form-group">
            <label for="details">상세 자기소개</label>
            <textarea id="details" v-model="formData.details" rows="6" placeholder="경력, 강점 등을 자유롭게 기술해주세요."></textarea>
          </div>

          <div class="form-group">
            <label for="experience">총 경력</label>
            <select id="experience" v-model="formData.experience">
              <option value="new">신입 (1년 미만)</option>
              <option value="1-3">1년 ~ 3년</option>
              <option value="3-5">3년 ~ 5년</option>
              <option value="5-10">5년 ~ 10년</option>
              <option value="10+">10년 이상</option>
            </select>
          </div>

          <div class="form-group">
            <label>보유 자격증</label>
            <div v-for="(cert, index) in formData.certifications" :key="index" class="dynamic-input-group">
              <input type="text" v-model="cert.name" placeholder="자격증명" class="cert-name">
              <input type="file" @change="e => handleCertFileChange(e, index)" class="cert-file">
              <button type="button" @click="removeCertification(index)" class="btn-remove">삭제</button>
            </div>
            <button type="button" @click="addCertification" class="btn-add">자격증 추가하기</button>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>희망 조건</legend>

          <div class="form-group">
            <label>돌봄 가능 유형</label>
            <div class="checkbox-group">
              <label><input type="checkbox" value="child" v-model="formData.careTypes"> 아동/영유아</label>
              <label><input type="checkbox" value="senior" v-model="formData.careTypes"> 노인/요양</label>
              <label><input type="checkbox" value="postpartum" v-model="formData.careTypes"> 산후조리</label>
              <label><input type="checkbox" value="sick" v-model="formData.careTypes"> 병간호/간병</label>
            </div>
          </div>

          <div class="form-group">
            <label>희망 근무 지역</label>
            <input type="text" v-model="formData.desiredArea" placeholder="예: 서울 강남구">
          </div>
        </fieldset>

        <div class="form-footer">
          <div class="checkbox-group single">
            <label>
              <input type="checkbox" v-model="formData.agreeToTerms" required>
              서비스 이용약관 및 개인정보 처리방침에 동의합니다.
            </label>
          </div>
          <button type="submit" class="btn-submit">지원서 제출하기</button>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const profilePreview = ref(null);
const formData = reactive({
  name: '', birthdate: '', contact: '', email: '', address: '',
  profilePicture: null, introduction: '', details: '', experience: 'new',
  certifications: [{ name: '', file: null }],
  careTypes: [], desiredArea: '', availableTimes: [], agreeToTerms: false
});

const handleProfileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    formData.profilePicture = file;
    const reader = new FileReader();
    reader.onload = (e) => { profilePreview.value = e.target.result; };
    reader.readAsDataURL(file);
  }
};

const addCertification = () => formData.certifications.push({ name: '', file: null });
const removeCertification = (index) => formData.certifications.splice(index, 1);
const handleCertFileChange = (event, index) => {
  if (event.target.files[0]) formData.certifications[index].file = event.target.files[0];
};

const handleSubmit = () => {
  if (!formData.agreeToTerms) { alert('약관에 동의해주세요.'); return; }
  console.log('선생님 지원 데이터:', formData);
  alert('지원서가 제출되었습니다.');
};
</script>

<style scoped>
.form-page-container {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.form-card {
  background-color: white;
  width: 100%;
  max-width: 700px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  overflow: hidden;
}


.form-header {
  padding: 40px 30px;
  text-align: center;
}
.form-header.primary-bg {
  background-color: #FFFBEB; /* 연한 노란 배경 */
  border-bottom: 1px solid #FCD34D;
}
.form-header h1 {
  color: #D97706;
  font-size: 28px;
  margin-bottom: 10px;
  font-weight: 800;
}
.form-header p {
  color: #92400E;
  font-size: 16px;
  line-height: 1.5;
}

.form-body {
  padding: 30px;
}

.form-section {
  border: none;
  padding: 0;
  margin: 0 0 40px 0;
}
.form-section legend {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  width: 100%;
  display: block;
}


.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.full-width {
  grid-column: span 2;
}

.form-group {
  display: flex;
  flex-direction: column;
}
label {
  font-size: 14px;
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
}
input[type="text"], input[type="tel"], input[type="email"], input[type="date"], select, textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.2s;
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #FBBF24;
}
textarea { resize: vertical; }


.profile-uploader {
  display: flex;
  align-items: center;
  gap: 20px;
}
.profile-preview {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #eee;
}
input[type="file"] { display: none; }
.btn-upload {
  padding: 8px 16px;
  background-color: #f1f3f5;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}
.btn-upload:hover { background-color: #e9ecef; }


.dynamic-input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}
.cert-name { flex: 1; }
.btn-remove {
  background: #ffcdd2;
  color: #c62828;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-add {
  width: 100%;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px dashed #ced4da;
  color: #868e96;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 5px;
}
.btn-add:hover { border-color: #FBBF24; color: #F59E0B; }


.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}
.checkbox-group label {
  display: flex;
  align-items: center;
  margin: 0;
  font-weight: normal;
  cursor: pointer;
}
.checkbox-group input { margin-right: 8px; }


.form-footer { margin-top: 30px; text-align: center; }
.btn-submit {
  background-color: #FBBF24;
  color: white;
  font-size: 18px;
  font-weight: 700;
  padding: 16px 40px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(251, 191, 36, 0.3);
  transition: transform 0.1s;
}
.btn-submit:hover { background-color: #F59E0B; transform: translateY(-2px); }


@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: auto; }
}
</style>