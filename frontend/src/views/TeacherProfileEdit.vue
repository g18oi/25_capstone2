<template>
  <div class="page-container">
    <div class="edit-card">
      <header class="edit-header">
        <h1> 선생님 프로필 수정</h1>
        <p>회원가입 시 입력했던 정보를 수정합니다.</p>
      </header>
      
      <form @submit.prevent="updateProfile" class="edit-body">
        
        <div class="form-section">
          <h3>기본 정보</h3>
          <div class="input-group">
            <label>이름</label>
            <input type="text" v-model="teacherInfo.name" disabled class="disabled-input" />
            <span class="hint">이름은 수정할 수 없습니다.</span>
          </div>

          <div class="input-group">
            <label>총 경력 기간</label>
            <select v-model="teacherInfo.experienceYear">
              <option value="" disabled>선택해주세요</option>
              <option value="new">신입 (1년 미만)</option>
              <option value="1-3">1년 ~ 3년 미만</option>
              <option value="3-5">3년 ~ 5년 미만</option>
              <option value="5-10">5년 ~ 10년 미만</option>
              <option value="10+">10년 이상</option>
            </select>
          </div>

          <div class="input-group">
            <label>경력 상세 내용</label>
            <textarea v-model="teacherInfo.experienceDesc" placeholder="주요 경력을 적어주세요."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h3>보유 자격증</h3>
          <div class="input-group">
            <div v-for="(cert, index) in teacherInfo.certifications" :key="index" class="cert-input-row">
              <input type="text" v-model="teacherInfo.certifications[index]" placeholder="자격증 이름">
              <button type="button" class="icon-btn remove" @click="removeCertification(index)">✕</button>
            </div>
            <button type="button" class="add-btn" @click="addCertification">+ 자격증 추가하기</button>
          </div>
        </div>

        <div class="form-section">
          <h3>활동 정보</h3>
          <div class="input-group">
            <label>가능한 활동 (중복 선택 가능)</label>
            <div class="checkbox-grid">
              <label v-for="activity in activityOptions" :key="activity">
                <input type="checkbox" :value="activity" v-model="teacherInfo.activities">
                <span>{{ activity }}</span>
              </label>
            </div>
          </div>

          <div class="input-group">
            <label>희망 활동 지역</label>
            <div class="address-group">
              <select v-model="regionSelect.province">
                <option value="" disabled>시/도</option>
                <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
              </select>
              <select v-model="regionSelect.district" :disabled="!regionSelect.province">
                <option value="" disabled>구/군</option>
                <option v-for="district in availableDistricts" :key="district" :value="district">{{ district }}</option>
              </select>
              <button type="button" class="address-btn" @click="addRegion" :disabled="!regionSelect.district">추가</button>
            </div>
            
            <div class="selected-tags-area" v-if="teacherInfo.selectedRegions.length > 0">
              <span v-for="region in teacherInfo.selectedRegions" :key="region" class="tag">
                {{ region }} <button type="button" @click="removeRegion(region)">x</button>
              </span>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3>근무 조건</h3>
          <div class="input-group">
            <label>희망 시급 (원)</label>
            <input type="text" :value="formatWage(teacherInfo.wage)" @input="onWageInput" placeholder="10,030" />
          </div>

          <div class="input-group">
            <label>자기소개 (Introduction)</label>
            <textarea v-model="teacherInfo.introduction" rows="4" placeholder="학부모님에게 보여질 소개글을 적어주세요."></textarea>
          </div>

          <div class="input-group">
            <label>CCTV 동의 여부</label>
            <div class="radio-group horizontal">
              <label :class="{ active: teacherInfo.cctvAgree === 'agree' }">
                <input type="radio" v-model="teacherInfo.cctvAgree" value="agree"> 동의함
              </label>
              <label :class="{ active: teacherInfo.cctvAgree === 'disagree' }">
                <input type="radio" v-model="teacherInfo.cctvAgree" value="disagree"> 동의안함
              </label>
            </div>
          </div>
        </div>

        <div class="button-group">
          <button type="button" class="btn-cancel" @click="$router.push('/teacher-home')">취소</button>
          <button type="submit" class="btn-save">수정 저장하기</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { regionData } from '../data/regions.js'; 

export default {
  data() {
    return {
      teacherInfo: {
        name: '',
        experienceYear: '',
        experienceDesc: '',
        certifications: [],
        activities: [],
        selectedRegions: [],
        wage: null,
        introduction: '',
        cctvAgree: 'agree'
      },
      regionData: regionData,
      regionSelect: { province: '', district: '' },
      activityOptions: ['실내놀이', '등하원 동행', '영어 놀이', '한글놀이', '학습지도', '야외활동', '책읽기']
    };
  },
  computed: {
    provinces() {
      return Object.keys(this.regionData);
    },
    availableDistricts() {
      if (!this.regionSelect.province) return [];
      return this.regionData[this.regionSelect.province] || [];
    }
  },
  watch: {
    'regionSelect.province'() {
      this.regionSelect.district = '';
    }
  },
  async mounted() {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
    if (!isLoggedIn) {
      alert('로그인이 필요합니다.');
      this.$router.push('/login');
      return;
    }


    await this.fetchTeacherData();
  },
  methods: {
async fetchTeacherData() {
  try {
    const response = await axios.get('/api/user/me', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'ngrok-skip-browser-warning': 'true'
      }
    });

    const data = response.data;
    console.log('불러온 정보:', data);

    this.teacherInfo = {
      name: data.name,
      experienceYear: data.career || '',
      experienceDesc: data.career_detail || '',
      certifications: data.certifications ? data.certifications.split(', ') : [],
      activities: data.activities ? data.activities.split(', ') : [],
      selectedRegions: data.hope_regions ? data.hope_regions.split(', ') : [],
      wage: data.hope_pay || null,
      introduction: data.introduction || '',
      cctvAgree: data.cctv_agree ? 'agree' : 'disagree'
    };

  } catch (error) {
    console.error('정보 로드 실패:', error);
    alert('회원 정보를 불러오지 못했습니다.');
  }
},


    addCertification() {
      this.teacherInfo.certifications.push('');
    },
    removeCertification(index) {
      this.teacherInfo.certifications.splice(index, 1);
    },


    addRegion() {
      const newRegion = `${this.regionSelect.province} - ${this.regionSelect.district}`;
      if (this.regionSelect.district && !this.teacherInfo.selectedRegions.includes(newRegion)) {
        this.teacherInfo.selectedRegions.push(newRegion);
      }
      this.regionSelect.district = '';
    },
    removeRegion(region) {
      this.teacherInfo.selectedRegions = this.teacherInfo.selectedRegions.filter(r => r !== region);
    },

    formatWage(value) {
      if (!value) return '';
      return Number(value).toLocaleString();
    },
    onWageInput(event) {
      const rawValue = event.target.value.replace(/[^0-9]/g, '');
      this.teacherInfo.wage = rawValue ? parseInt(rawValue, 10) : null;
      event.target.value = this.formatWage(this.teacherInfo.wage);
    },

   
async updateProfile() {
  if (!confirm('프로필을 수정하시겠습니까?')) return;

  try {

    const payload = {
        career: this.teacherInfo.experienceYear,
        career_detail: this.teacherInfo.experienceDesc,
        certifications: this.teacherInfo.certifications.filter(c => c.trim() !== ''),
        activities: this.teacherInfo.activities,
        hope_regions: this.teacherInfo.selectedRegions,
        hope_pay: this.teacherInfo.wage,
        introduction: this.teacherInfo.introduction,
        cctv_agree: this.teacherInfo.cctvAgree === 'agree'
    };

    await axios.put('/api/user/update', payload, {
      headers: { 
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'ngrok-skip-browser-warning': 'true' 
      }
    });

    alert('성공적으로 수정되었습니다!');
    this.$router.push('/teacher-home');

  } catch (error) {
    console.error('수정 실패:', error);
    alert('수정 중 오류가 발생했습니다.');
  }
}
  }
};
</script>

<style scoped>
.page-container { display: flex; justify-content: center; padding: 40px 20px; background-color: #f8f9fa; min-height: 100vh; }
.edit-card { width: 100%; max-width: 600px; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }

.edit-header { background-color: #4CAF50; color: white; padding: 25px; text-align: center; }
.edit-header h1 { margin: 0 0 10px 0; font-size: 1.5rem; }
.edit-header p { margin: 0; opacity: 0.9; font-size: 0.95rem; }

.edit-body { padding: 30px; }

.form-section { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
.form-section:last-child { border-bottom: none; }
.form-section h3 { font-size: 1.1rem; color: #4CAF50; margin-bottom: 15px; font-weight: 700; border-left: 4px solid #4CAF50; padding-left: 10px; }

.input-group { margin-bottom: 20px; }
.input-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; font-size: 0.95rem; }
.input-group input, .input-group select, .input-group textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.input-group input:focus, .input-group select:focus, .input-group textarea:focus { outline: none; border-color: #4CAF50; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1); }
.disabled-input { background-color: #f5f5f5; color: #888; cursor: not-allowed; }
.hint { font-size: 0.8rem; color: #888; margin-top: 4px; display: block; }

.cert-input-row { display: flex; gap: 8px; margin-bottom: 8px; }
.icon-btn.remove { background: #ffebee; color: #d32f2f; border: none; width: 40px; border-radius: 8px; cursor: pointer; font-weight: bold; }
.add-btn { width: 100%; padding: 10px; background-color: #f1f8e9; color: #2e7d32; border: 1px dashed #4CAF50; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.2s; }
.add-btn:hover { background-color: #e8f5e9; }


.checkbox-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.checkbox-grid label { display: inline-flex; align-items: center; cursor: pointer; background: #f8f9fa; padding: 8px 12px; border-radius: 20px; border: 1px solid #eee; transition: 0.2s; }
.checkbox-grid input { display: none; }
.checkbox-grid label:has(input:checked) { background: #e8f5e9; border-color: #4CAF50; color: #2e7d32; font-weight: bold; }

.address-group { display: flex; gap: 8px; margin-bottom: 10px; }
.address-group select { flex: 1; }
.address-btn { padding: 0 20px; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
.address-btn:disabled { background: #ccc; cursor: not-allowed; }

.selected-tags-area { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { background: #e8f5e9; color: #2e7d32; padding: 5px 12px; border-radius: 15px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; }
.tag button { background: none; border: none; color: #2e7d32; cursor: pointer; font-weight: bold; font-size: 1rem; padding: 0; }

.radio-group.horizontal { display: flex; gap: 10px; }
.radio-group label { flex: 1; text-align: center; padding: 12px; border: 1px solid #ddd; border-radius: 8px; cursor: pointer; transition: 0.2s; }
.radio-group input { display: none; }
.radio-group label.active { background: #e8f5e9; border-color: #4CAF50; color: #2e7d32; font-weight: bold; }

.button-group { display: flex; gap: 10px; margin-top: 30px; }
.button-group button { flex: 1; padding: 14px; border: none; border-radius: 8px; font-size: 1rem; font-weight: bold; cursor: pointer; }
.btn-cancel { background-color: #e9ecef; color: #555; }
.btn-save { background-color: #4CAF50; color: white; box-shadow: 0 4px 6px rgba(76, 175, 80, 0.2); }
.btn-save:hover { background-color: #43A047; }
</style> 