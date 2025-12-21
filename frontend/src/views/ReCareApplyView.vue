<template>
  <div class="form-page-container">
    <div class="form-card">
      
      <header class="form-header">
        <h2>돌보미 매칭 신청하기</h2>
        <p>돌봄이 필요한 아동의 정보와 요청 사항을 입력해주세요.<br>ReCare가 최적의 선생님을 찾아 드립니다.</p>
      </header>

      <form @submit.prevent="handleSubmitApplication" class="form-body">

        <fieldset class="form-section">
          <legend>1. 신청자(학부모) 정보</legend>
          <div class="form-grid">
            <div class="form-group">
              <label for="parentName">신청자 성명</label>
              <input type="text" id="parentName" v-model="form.parentName" placeholder="예) 홍길동" required />
            </div>
            <div class="form-group">
              <label for="contact">연락처</label>
              <input type="tel" id="contact" v-model="form.contact" placeholder="010-1234-5678" required />
            </div>
            <div class="form-group full-width">
              <label for="address">돌봄 주소</label>
              <input type="text" id="address" v-model="form.address" placeholder="주소를 입력하세요" required />
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>2. 아동 정보</legend>
          <div class="form-grid">
            <div class="form-group full-width">
              <label for="childName">아동 이름</label>
              <input type="text" id="childName" v-model="form.childName" required />
            </div>
            
            <div class="form-group">
              <label for="childAge">나이 (만)</label>
              <input type="number" id="childAge" v-model.number="form.childAge" min="0" placeholder="숫자만 입력" required />
            </div>
            
            <div class="form-group">
              <label>성별</label>
              <div class="radio-group">
                <div class="checkbox-group" style="border:none; background:none; padding:0;">
                  <label><input type="radio" value="남" v-model="form.childGender" required> 남아</label>
                  <label><input type="radio" value="여" v-model="form.childGender"> 여아</label>
                </div>
              </div>
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>3. 돌봄 요청 정보</legend>
          <div class="form-grid">
            <div class="form-group">
              <label for="careType">돌봄 유형</label>
              <select id="careType" v-model="form.careType" required>
                <option disabled value="">유형 선택</option>
                <option value="full-time">종일 돌봄</option>
                <option value="part-time">시간제 돌봄</option>
                <option value="school-pickup">등/하원 도우미</option>
                <option value="emergency">긴급/단기 돌봄</option>
              </select>
            </div>
            <div class="form-group">
              <label for="startDate">희망 시작일</label>
              <input type="date" id="startDate" v-model="form.startDate" required />
            </div>
            <div class="form-group full-width">
              <label for="careSchedule">필요한 요일 및 시간</label>
              <textarea id="careSchedule" v-model="form.careSchedule" rows="3" placeholder="예) 월, 수, 금 / 15:00 ~ 19:00"></textarea>
            </div>
            <div class="form-group full-width">
              <label for="specialNotes">특이사항 및 요청사항</label>
              <textarea id="specialNotes" v-model="form.specialNotes" rows="5" placeholder="아이의 알레르기, 성향 등 상세 요청사항"></textarea>
            </div>
          </div>
        </fieldset>

        <div class="form-footer">
          <button type="submit" class="btn-submit">매칭 신청서 제출하기</button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReCareApply',
  data() {
    return {
      form: {
        parentName: '',
        contact: '',
        address: '',
        childName: '',
        childAge: null,
        childGender: '',
        careType: '',
        startDate: '',
        careSchedule: '',
        specialNotes: ''
      }
    };
  },
  methods: {
    handleSubmitApplication() {
      if (!this.form.childGender) {
        alert('아동 성별을 선택해주세요.');
        return;
      }
      console.log('학부모 신청 데이터:', this.form);
      alert('신청서가 제출되었습니다.');
    }
  }
}
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
  max-width: 650px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  overflow: hidden;
}

.form-header {
  padding: 40px 30px 20px;
  text-align: center;
}
.form-header h2 {
  font-size: 26px;
  font-weight: 800;
  color: #333;
  margin-bottom: 10px;
}
.form-header p {
  color: #666;
  font-size: 15px;
  line-height: 1.5;
}


.form-body { padding: 30px; }

.form-section {
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 25px;
}
.form-section legend {
  font-size: 16px;
  font-weight: 700;
  color: #F59E0B; /* 포인트 컬러 */
  padding: 0 10px;
}


.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}
.full-width { grid-column: span 2; }

.form-group { display: flex; flex-direction: column; }
label {
  font-size: 14px;
  color: #495057;
  margin-bottom: 6px;
  font-weight: 600;
}
input, select, textarea {
  padding: 12px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 15px;
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #FBBF24;
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.1);
}


.radio-group .checkbox-group {
  display: flex;
  gap: 20px;
}
.radio-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}
.radio-group input { margin-right: 6px; }


.form-footer { margin-top: 10px; text-align: center; }
.btn-submit {
  width: 100%;
  background-color: #333;
  color: white;
  font-size: 16px;
  font-weight: 700;
  padding: 18px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-submit:hover { background-color: #000; }

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: auto; }
}
</style>