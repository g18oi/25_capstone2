<template>
  <div class="main-layout">
    <TheHeader />
    <main class="auth-layout">
      <div class="signup-card">
        <div class="logo">
          <span class="logo-icon">🔗</span>
          <span class="logo-text">아이Link</span>
        </div>
        <p class="tagline">새로운 계정 만들기</p>

        <div class="user-type-selector">
          <label :class="{ active: userType === 'parent' }">
            <input type="radio" v-model="userType" value="parent" name="userType">
            <span>👨‍👩‍👧‍👦 학부모</span>
          </label>
          <label :class="{ active: userType === 'sitter' }">
            <input type="radio" v-model="userType" value="sitter" name="userType">
            <span>👩‍🏫 돌봄선생님</span>
          </label>
        </div>

        <div class="input-group">
          <label for="name">이름 (실명)</label>
          <input type="text" id="name" v-model="name" placeholder="홍길동" />
        </div>

        <div class="input-group">
          <label for="identifier">이메일 (아이디)</label>
          <input type="email" id="identifier" v-model="identifier" placeholder="example@email.com" />
        </div>

        <div class="input-group">
          <label for="password">비밀번호 <span class="hint-text">(영문, 숫자 포함 6자 이상)</span></label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="비밀번호를 입력하세요" 
            @input="resetPasswordError"
          />
        </div>

        <div class="input-group">
          <label for="confirmPassword">비밀번호 확인</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            placeholder="비밀번호를 한 번 더 입력하세요" 
            @input="resetPasswordError"
          />
          <p v-if="passwordError" class="error-message">🚨 {{ passwordError }}</p>
        </div>

        <hr>

        <div v-if="userType === 'parent'" class="conditional-section">
          <p class="section-title">학부모님 정보 입력</p>

          <div class="input-group">
            <label>아이 수 (명)</label>
            <div class="counter-box">
              <button type="button" class="counter-btn" @click="decreaseChildCount" :disabled="parentInfo.numChildren <= 1">
                −
              </button>
              <span class="count-display">{{ parentInfo.numChildren }}명</span>
              <button type="button" class="counter-btn" @click="increaseChildCount" :disabled="parentInfo.numChildren >= 10">
                +
              </button>
            </div>
          </div>

          <div v-for="(child, index) in parentInfo.children" :key="index" class="child-info-box">
            <p class="child-info-title">{{ index + 1 }}번째 아이 정보</p>
            <div class="input-group-row">
              <div class="input-group">
                <label :for="'birthYear' + index">출생년도</label>
                <select :id="'birthYear' + index" v-model="child.birthYear">
                  <option disabled value="">선택</option>
                  <option v-for="year in birthYears" :key="year" :value="year">{{ year }}년</option>
                </select>
              </div>
              <div class="input-group">
                <label :for="'age' + index">나이 (만)</label>
                <input type="number" :id="'age' + index" v-model="child.age" placeholder="자동 계산" readonly />
              </div>
            </div>
            <div class="input-group" style="margin-bottom: 0;">
              <label>성별</label>
              <div class="radio-group horizontal small">
                <label :class="{ active: child.gender === 'male' }">
                  <input type="radio" v-model="child.gender" value="male"> 남아 👦
                </label>
                <label :class="{ active: child.gender === 'female' }">
                  <input type="radio" v-model="child.gender" value="female"> 여아 👧
                </label>
              </div>
            </div>
          </div>
          
          <div class="input-group">
            <label>거주 지역</label>
            <div class="input-group-row">
              <select v-model="parentInfo.selectedProvince" @change="onParentProvinceChange">
                <option value="" disabled>시/도</option>
                <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
              </select>
              <select v-model="parentInfo.selectedDistrict" :disabled="!parentInfo.selectedProvince">
                <option value="" disabled>구/군</option>
                <option v-for="district in districtsForParent" :key="district" :value="district">{{ district }}</option>
              </select>
            </div>
            <input type="text" v-model="parentInfo.detailAddress" placeholder="상세 주소 (선택)" style="margin-top: 10px;">
          </div>

          <div class="input-group">
            <label for="parentWage">희망 시급 <span class="hint-text">(2025년 최저: 10,030원)</span></label>
            <div class="wage-input-wrapper">
              <input type="text" id="parentWage" :value="formatWage(parentInfo.wage)" @input="e => onWageInput(e, parentInfo)" placeholder="10,030">
              <div class="checkbox-wrapper">
                <input type="checkbox" id="wageNegotiableParent" v-model="parentInfo.wageNegotiable">
                <label for="wageNegotiableParent" class="no-wrap-label">시급협의 가능</label>
              </div>
            </div>
          </div>

          <div class="input-group">
            <label>어떤 돌봄을 원하세요?</label>
            <div class="checkbox-grid">
              <label v-for="care in careOptions" :key="care">
                <input type="checkbox" :value="care" v-model="parentInfo.careTypes" @change="checkCareLimit">
                <span>{{ care }}</span>
              </label>
            </div>
          </div>

          <div class="input-group">
            <label for="parentNotes">선생님이 알아야 할 내용 (선택)</label>
            <textarea id="parentNotes" v-model="parentInfo.notes" placeholder="아이 성격, 알레르기 등"></textarea>
          </div>
        </div>

        <div v-if="userType === 'sitter'" class="conditional-section">
          <p class="section-title">선생님 정보 입력</p>

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
            <label for="experienceDesc">경력 상세 내용</label>
            <textarea id="experienceDesc" v-model="teacherInfo.experienceDesc" placeholder="주요 경력을 적어주세요."></textarea>
          </div>

          <div class="input-group">
            <label>보유 자격증 <span class="hint-text">(선택)</span></label>
            <div v-for="(cert, index) in teacherInfo.certifications" :key="index" class="cert-input-row">
              <input type="text" v-model="teacherInfo.certifications[index]" placeholder="자격증 이름">
              <button class="icon-btn remove" @click="removeCertification(index)">✕</button>
            </div>
            <button class="add-btn" @click="addCertification">+ 자격증 추가하기</button>
          </div>

          <div class="input-group">
            <label>가능한 활동</label>
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
              <select v-model="teacherRegionSelect.province">
                <option value="" disabled>시/도</option>
                <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
              </select>
              <select v-model="teacherRegionSelect.district" :disabled="!teacherRegionSelect.province">
                <option value="" disabled>구/군</option>
                <option v-for="district in districtsForTeacher" :key="district" :value="district">{{ district }}</option>
              </select>
              <button class="address-btn" @click="addTeacherRegion" :disabled="!teacherRegionSelect.district">추가</button>
            </div>

            <div style="margin-top: 10px;">
              <button type="button" class="location-btn" @click="verifyLocation" :disabled="teacherInfo.selectedRegions.length === 0">
                📍 내 위치와 일치하는지 확인하기
              </button>
              <p v-if="locationStatus.message" :class="['status-msg', locationStatus.success ? 'success' : 'error']">
                {{ locationStatus.message }}
              </p>
            </div>

            <div class="selected-tags-area" v-if="teacherInfo.selectedRegions.length > 0">
              <span v-for="region in teacherInfo.selectedRegions" :key="region" class="tag">
                {{ region }} <button @click="removeTeacherRegion(region)">x</button>
              </span>
            </div>
          </div>

          <div class="input-group">
            <label for="teacherWage">희망 시급</label>
            <input type="text" id="teacherWage" :value="formatWage(teacherInfo.wage)" @input="e => onWageInput(e, teacherInfo)" placeholder="10,030">
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

        <div class="terms-container">
          <label class="terms-label">개인정보 처리방침</label>
          <div class="terms-scroll-box">
            <p class="terms-title">제1조 (수집하는 개인정보 항목)</p>
            <p>회사는 회원가입, 상담, 서비스 신청 등을 위해 아래와 같은 개인정보를 수집하고 있습니다.</p>
            <ul class="terms-list">
              <li><strong>1. 학부모 회원</strong>
                <ul>
                  <li>필수항목: 이름, 이메일(아이디), 비밀번호, 휴대전화번호, 주소</li>
                  <li>자녀정보: 자녀의 이름, 생년월일, 성별, 돌봄 요청사항</li>
                  <li>매칭정보: 희망 시급, 희망 돌봄 유형</li>
                </ul>
              </li>
              <li><strong>2. 선생님 회원</strong>
                <ul>
                  <li>필수항목: 이름, 이메일(아이디), 비밀번호, 생년월일, 휴대전화번호, 주소</li>
                  <li>자격정보: 프로필 사진, 자격증 사본, 경력사항, 자기소개</li>
                  <li>매칭정보: 희망 시급, 활동 가능 지역, CCTV 동의 여부</li>
                </ul>
              </li>
              <li><strong>3. 서비스 이용 과정에서 자동 수집</strong>
                <ul>
                  <li>IP 주소, 쿠키, 방문 일시, 서비스 이용 기록, 기기정보</li>
                  <li>위치정보 (위치기반 서비스 이용 시)</li>
                </ul>
              </li>
            </ul>

            <p class="terms-title">제2조 (개인정보의 수집 및 이용목적)</p>
            <p>회사는 수집한 개인정보를 다음의 목적을 위해 활용합니다.</p>
            <ul class="terms-list">
              <li><strong>1. 서비스 제공 및 계약 이행</strong><br>아이돌봄 교사 매칭, 콘텐츠 제공, 본인인증, 구매 및 요금 결제</li>
              <li><strong>2. 회원 관리</strong><br>회원제 서비스 이용에 따른 본인확인, 개인식별, 가입의사 확인, 연령확인, 불만처리 등 민원처리</li>
              <li><strong>3. 신규 서비스 개발 및 마케팅</strong><br>신규 서비스 개발, 통계학적 특성에 따른 서비스 제공, 접속 빈도 파악</li>
            </ul>

            <p class="terms-title">제3조 (개인정보의 보유 및 이용기간)</p>
            <p>원칙적으로 개인정보 수집 및 이용목적이 달성된 후에는 해당 정보를 지체 없이 파기합니다. 단, 관계법령의 규정에 의하여 보존할 필요가 있는 경우 회사는 관계법령에서 정한 일정한 기간 동안 회원정보를 보관합니다.</p>
          </div>
          <div class="agreement-section">
            <input type="checkbox" id="agree" v-model="agreed" />
            <label for="agree">위 개인정보 처리방침을 확인하였으며, 이에 동의합니다.</label>
          </div>
        </div>

        <BaseButton @click="signUp" type="primary" :disabled="!agreed || isSubmitting">
          {{ isSubmitting ? '가입 처리 중...' : '가입하기' }}
        </BaseButton>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'; 
import BaseButton from '../components/BaseButton.vue';
import TheHeader from '../components/TheHeader.vue';
import { regionData } from '../data/regions.js';

export default {
  emits: ['show-modal'],
  components: { BaseButton, TheHeader },
  data() {
    return {
      isSubmitting: false,
      name: '',
      identifier: '',
      userType: 'parent',
      password: '',
      confirmPassword: '',
      passwordError: '',
      agreed: false,
      regionData: regionData,

      locationStatus: {
        success: false,
        message: ''
      },

      parentInfo: {
        numChildren: 1,
        children: [{ birthYear: '', age: '', gender: '' }],
        selectedProvince: '',
        selectedDistrict: '',
        detailAddress: '',
        wage: null,
        wageNegotiable: false,
        careTypes: [],
        notes: ''
      },

      teacherInfo: {
        experienceYear: '', 
        experienceDesc: '',
        certifications: [],
        activities: [],
        selectedRegions: [],
        wage: null,
        paymentCycles: ['월급'], 
        cctvAgree: '',
        notes: ''
      },
      teacherRegionSelect: { province: '', district: '' },
      
      careOptions: ['실내놀이', '등하원 동행', '영어 놀이', '한글놀이', '학습지도', '야외활동', '책읽기'],
      activityOptions: ['실내놀이', '등하원 동행', '영어 놀이', '한글놀이', '학습지도', '야외활동', '책읽기'],
      paymentCycles: ['일급', '주급', '월급'],
    };
  },
  computed: {
    birthYears() {
      const startYear = 2010;
      const endYear = new Date().getFullYear();
      let years = [];
      for (let i = endYear; i >= startYear; i--) years.push(i);
      return years;
    },
    provinces() { return Object.keys(this.regionData); },
    districtsForParent() {
      if (!this.parentInfo.selectedProvince) return [];
      return this.regionData[this.parentInfo.selectedProvince] || [];
    },
    districtsForTeacher() {
      if (!this.teacherRegionSelect.province) return [];
      return this.regionData[this.teacherRegionSelect.province] || [];
    }
  },
  watch: {
    'teacherRegionSelect.province'() { this.teacherRegionSelect.district = ''; },
    'parentInfo.numChildren'(newCount) {
      if (!newCount || newCount < 0) return;
      if (newCount > 10) {
        alert("최대 10명까지만 입력 가능합니다.");
        this.parentInfo.numChildren = 10;
        return;
      }
      const currentLength = this.parentInfo.children.length;
      if (newCount > currentLength) {
        const diff = newCount - currentLength;
        for (let i = 0; i < diff; i++) this.parentInfo.children.push({ birthYear: '', age: '', gender: '' });
      } else if (newCount < currentLength) {
        this.parentInfo.children.splice(newCount);
      }
    },
    'parentInfo.children': {
      handler(newChildren) {
        const currentYear = new Date().getFullYear();
        newChildren.forEach(child => {
          if (child.birthYear) child.age = currentYear - child.birthYear;
          else child.age = '';
        });
      },
      deep: true
    }
  },
  methods: {
    decreaseChildCount() {
      if (this.parentInfo.numChildren > 1) {
        this.parentInfo.numChildren--;
      }
    },
    increaseChildCount() {
      if (this.parentInfo.numChildren < 10) {
        this.parentInfo.numChildren++;
      }
    },
    addCertification() { this.teacherInfo.certifications.push(''); },
    removeCertification(index) { this.teacherInfo.certifications.splice(index, 1); },
    resetPasswordError() { this.passwordError = ''; },
    formatWage(value) {
      if (!value) return '';
      return Number(value).toLocaleString();
    },
    onWageInput(event, targetInfo) {
      const rawValue = event.target.value.replace(/[^0-9]/g, '');
      if (rawValue) {
        targetInfo.wage = parseInt(rawValue, 10);
        event.target.value = targetInfo.wage.toLocaleString();
      } else {
        targetInfo.wage = null;
        event.target.value = '';
      }
    },
    onParentProvinceChange() { this.parentInfo.selectedDistrict = ''; },
    addTeacherRegion() {
      const newRegion = `${this.teacherRegionSelect.province} - ${this.teacherRegionSelect.district}`;
      if (this.teacherRegionSelect.district && !this.teacherInfo.selectedRegions.includes(newRegion)) {
        this.teacherInfo.selectedRegions.push(newRegion);
      }
      this.teacherRegionSelect.district = '';
    },
    removeTeacherRegion(regionToRemove) {
      this.teacherInfo.selectedRegions = this.teacherInfo.selectedRegions.filter(r => r !== regionToRemove);
    },
    checkCareLimit() {
      if (this.parentInfo.careTypes.length > 3) {
        this.$emit('show-modal', { message: '돌봄 종류는 최대 3개까지 선택 가능합니다.', onConfirm: ()=>{} });
        this.parentInfo.careTypes.pop();
      }
    },

    async verifyLocation() {
      if (this.teacherInfo.selectedRegions.length === 0) {
        alert("먼저 희망 활동 지역을 선택해서 추가해주세요.");
        return;
      }

      this.locationStatus = { success: false, message: '위치 정보를 가져오는 중...' };

      if (!("geolocation" in navigator)) {
        this.locationStatus = { success: false, message: '이 브라우저는 위치 정보를 지원하지 않습니다.' };
        return;
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            console.log(`위도: ${lat}, 경도: ${lon}`);

            const actualAddress = await this.mockReverseGeocoding(lat, lon); 

            const selectedRegion = this.teacherInfo.selectedRegions[0];

            const response = await axios.post('/api/auth/region-check', {
              address: actualAddress,
              regions: selectedRegion
            });

            if (response.data.match) {
              this.locationStatus = { success: true, message: ' 인증 성공: 현재 위치와 활동 지역이 일치합니다.' };
            } else {
              this.locationStatus = { success: false, message: ` 인증 실패: 실제 위치(${actualAddress})가 다릅니다.` };
            }

          } catch (error) {
            console.error(error);
            this.locationStatus = { success: false, message: '위치 확인 중 오류가 발생했습니다.' };
          }
        },
        (error) => {
          console.error(error);
          this.locationStatus = { success: false, message: '위치 정보 접근이 거부되었습니다.' };
        }
      );
    },

async mockReverseGeocoding(lat, lon) {
  try {
    const response = await axios.get('https://nominatim.openstreetmap.org/reverse', {
      params: {
        format: 'json',
        lat: lat,
        lon: lon,
        zoom: 18,
        addressdetails: 1,
        'accept-language': 'ko'
      }
    });

    if (response.data && response.data.address) {
      const addr = response.data.address;
      
      let province = addr.province || addr.state || '';
      let city = addr.city || addr.county || '';
      let district = addr.district || addr.borough || addr.suburb || '';

      if (!province && city) {
         province = city;
         city = district; 
      }

      if (province && city) {
         return `${province} - ${city}`;
      }

      return (province || city).trim();
    }
    
    return "주소 확인 불가";

  } catch (error) {
    console.error(error);
    return '위치 확인 에러';
  }
},

    validateInputs() {
      if (!this.name) return false;
      if (!this.identifier) return false;
      if (!this.password) return false;
      if (!this.confirmPassword) return false;

      if (this.userType === 'parent') {
        if (!this.parentInfo.numChildren) return false;
        for (const child of this.parentInfo.children) {
          if (!child.birthYear || !child.gender) return false;
        }
        if (!this.parentInfo.selectedProvince || !this.parentInfo.selectedDistrict) return false;
        if (!this.parentInfo.wage) return false;
        if (this.parentInfo.careTypes.length === 0) return false;
      } 
     
      else if (this.userType === 'sitter') {
        if (!this.teacherInfo.experienceYear) return false;
        if (!this.teacherInfo.experienceDesc) return false;
        if (this.teacherInfo.activities.length === 0) return false;
        if (this.teacherInfo.selectedRegions.length === 0) return false;
        if (!this.teacherInfo.wage) return false;
        if (!this.teacherInfo.cctvAgree) return false;
      }
      return true;
    },
    
    async signUp() {
      if (this.isSubmitting) return;

      if (!this.validateInputs()) {
        alert('이름, 이메일 등 필수 정보를 모두 입력했는지 확인해주세요.');
        return;
      }
      const passwordRegex = /^(?=.*[a-zA-Z])(?=.*[0-9]).+$/;
      if (!this.password || !passwordRegex.test(this.password) || this.password.length < 6) {
        this.passwordError = '비밀번호는 영문과 숫자를 포함하여 6자 이상이어야 합니다.';
        return;
      }
      if (this.password !== this.confirmPassword) {
        this.passwordError = '비밀번호가 일치하지 않습니다.';
        this.confirmPassword = ''; 
        return;
      }
      if (!this.agreed) {
        alert('개인정보 활용에 동의해야 합니다.');
        return;
      }
      
     
      if (this.userType === 'sitter') {
        this.teacherInfo.certifications = this.teacherInfo.certifications.filter(c => c.trim() !== '');
      }

      this.isSubmitting = true;

      try {
        const numericWage = this.userType === 'parent' 
          ? Number(String(this.parentInfo.wage).replace(/,/g, '')) 
          : Number(String(this.teacherInfo.wage).replace(/,/g, ''));

        let fullAddress = '';
        let regionValue = '';

        if (this.userType === 'parent') {
          fullAddress = `${this.parentInfo.selectedProvince} ${this.parentInfo.selectedDistrict} ${this.parentInfo.detailAddress}`.trim();
          regionValue = [`${this.parentInfo.selectedProvince} ${this.parentInfo.selectedDistrict}`];
        } else {
          fullAddress = this.teacherInfo.selectedRegions[0] || '주소 미입력';
          regionValue = this.teacherInfo.selectedRegions;
        }

        let childrenProfiles = null;
        if (this.userType === 'parent') {
          childrenProfiles = this.parentInfo.children.map(child => ({
            child_year: String(child.birthYear),
            child_age: Number(child.age),
            child_gender: child.gender
          }));
        }

        const formData = {
          name: this.name,
          email: this.identifier,
          password1: this.password,
          password2: this.confirmPassword,
          role: this.userType,
          address: fullAddress,

          hope_pay: numericWage,
          
          hope_regions: regionValue,

          activities: this.userType === 'parent' ? this.parentInfo.careTypes : this.teacherInfo.activities,

          children_profiles: childrenProfiles,
          
          warning: this.userType === 'parent' ? this.parentInfo.notes : null,
          
          pay_period: this.userType === 'sitter' ? this.teacherInfo.paymentCycles : null,
          
          cctv_agree: this.userType === 'sitter' ? (this.teacherInfo.cctvAgree === 'agree') : null,
          info_agree: this.agreed,
          
          career: this.userType === 'sitter' ? this.teacherInfo.experienceYear : null,
          career_detail: this.userType === 'sitter' ? this.teacherInfo.experienceDesc : null,
          certifications: this.userType === 'sitter' ? this.teacherInfo.certifications.filter(c => c.trim() !== '') : null,
          introduction: this.userType === 'sitter' ? this.teacherInfo.notes : null
        };

        const response = await axios.post('/api/auth/signup', formData, {
          headers: { 'ngrok-skip-browser-warning': 'true' }
        });

        if (response.status === 200 || response.status === 201) {
          this.$emit('show-modal', {
            message: '회원가입 성공! 로그인 해주세요.',
            onConfirm: () => this.$router.push('/login')
          });
        }

      } catch (error) {
        if (error.response) {
          console.error('서버 에러 상세:', error.response.data);
          
          if (error.response.status === 500) {
            alert('서버 내부 오류가 발생했습니다.\n입력 데이터를 다시 확인하거나 다른 이메일로 시도해보세요.');
          } else {
            const errorDetail = error.response.data.detail;
            let alertMsg = '';
            if (Array.isArray(errorDetail)) {
              alertMsg = errorDetail.map(e => {
                const field = e.loc[e.loc.length - 1];
                return `${field}: ${e.msg}`;
              }).join('\n');
            } else {
              alertMsg = errorDetail || '회원가입 중 오류가 발생했습니다.';
            }
            alert('가입 실패:\n' + alertMsg);
          }
        } else {
          alert('서버와 연결할 수 없습니다.');
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.auth-layout { display: flex; justify-content: center; align-items: center; padding: 60px 20px; min-height: calc(100vh - 75px); background-color: #f8f9fa; }
.signup-card { width: 100%; max-width: 560px; padding: 40px; background-color: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); text-align: center; }
.logo { display: flex; justify-content: center; align-items: center; margin-bottom: 15px; }
.logo-icon { font-size: 38px; margin-right: 10px; color: #FBBF24; }
.logo-text { font-size: 36px; font-weight: 800; color: #333; }
.tagline { font-size: 18px; color: #666; margin-bottom: 30px; }
.input-group { text-align: left; margin-bottom: 22px; }
.input-group label { display: block; font-size: 14px; color: #555; margin-bottom: 8px; font-weight: 500; }
.input-group input, .input-group textarea, .input-group select { width: 100%; padding: 14px; border: 1px solid #e0e0e0; border-radius: 10px; font-size: 16px; box-sizing: border-box; transition: border-color 0.2s, box-shadow 0.2s; }
.input-group input:focus, .input-group textarea:focus, .input-group select:focus { outline: none; border-color: #FBBF24; box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.2); }
.input-group input:read-only { background-color: #f8f9fa; color: #868e96; }
.input-group input::placeholder, .input-group textarea::placeholder { color: #adb5bd; }
textarea { resize: vertical; min-height: 80px; }
hr { border: none; border-top: 1px solid #eee; margin: 30px 0; }
.user-type-selector { display: flex; justify-content: space-between; margin-bottom: 30px; border-radius: 12px; overflow: hidden; border: 1px solid #e0e0e0; }
.user-type-selector label { flex: 1; padding: 15px; text-align: center; cursor: pointer; transition: background-color 0.3s; font-weight: 500; }
.user-type-selector input[type="radio"] { display: none; }
.user-type-selector label.active { background-color: #FFFBEB; color: #F59E0B; font-weight: 700; }
.conditional-section { margin-top: 20px; }
.section-title { font-size: 18px; font-weight: 600; color: #333; margin-bottom: 20px; text-align: left; border-left: 4px solid #FBBF24; padding-left: 10px; }
.hint-text { color: #868e96; font-weight: 400; font-size: 13px; margin-left: 8px; display: inline; }
.radio-group label { margin-right: 20px; }
.child-info-box { border: 1px solid #f0f0f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; animation: fadeIn 0.3s ease-out; }
.child-info-title { font-weight: 600; text-align: left; margin-bottom: 15px; }
.input-group-row { display: flex; gap: 15px; }
.input-group-row select { flex: 1; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

.wage-input-wrapper { display: flex; align-items: center; gap: 10px; }
.checkbox-wrapper { display: flex; align-items: center; flex-shrink: 0; }
.checkbox-wrapper input[type="checkbox"] { margin-right: 8px; }
.no-wrap-label { white-space: nowrap; font-size: 15px; }

.checkbox-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.checkbox-grid label { display: inline-block; }
.checkbox-grid input[type="checkbox"] { display: none; }
.checkbox-grid span { display: inline-block; padding: 10px 16px; border: 1px solid #e0e0e0; border-radius: 20px; font-size: 15px; cursor: pointer; transition: all 0.2s ease; user-select: none; }
.checkbox-grid input[type="checkbox"]:checked + span { background-color: #FFFBEB; color: #F59E0B; border-color: #FBBF24; font-weight: 600; }
.checkbox-grid label:hover span { border-color: #FBBF24; }
.radio-group.horizontal { display: flex; gap: 10px; border: 1px solid #e0e0e0; border-radius: 12px; overflow: hidden; margin-top: 5px; }
.radio-group.horizontal label { flex: 1; padding: 14px; text-align: center; cursor: pointer; transition: background-color 0.3s; font-weight: 500; margin: 0; }
.radio-group.horizontal input[type="radio"] { display: none; }
.radio-group.horizontal label.active { background-color: #FFFBEB; color: #F59E0B; font-weight: 700; }
.radio-group.horizontal.small label { padding: 10px; font-size: 15px; }
.address-group { display: flex; gap: 10px; }
.address-group select { flex: 1; }
.address-btn { padding: 0 20px; border: 1px solid #ddd; background-color: #f8f8f8; border-radius: 10px; cursor: pointer; font-size: 14px; font-weight: 500; }
.address-btn:hover { background-color: #f0f0f0; }
.address-btn:disabled { background-color: #f8f9fa; cursor: not-allowed; color: #adb5bd; }
.selected-tags-area { margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 8px; min-height: 40px; }
.tag { display: inline-block; background-color: #FFFBEB; color: #F59E0B; border: 1px solid #FBBF24; padding: 5px 12px; border-radius: 15px; font-size: 14px; margin-right: 8px; margin-bottom: 8px; font-weight: 500; }
.tag button { background: none; border: none; color: #F59E0B; cursor: pointer; margin-left: 4px; font-weight: bold; font-size: 14px; padding: 0; }
.error-message { color: #e53935; font-size: 13px; margin-top: 8px; font-weight: bold; }
.terms-container { margin-bottom: 20px; text-align: left; }
.terms-label { display: block; font-size: 15px; font-weight: 600; color: #333; margin-bottom: 8px; }
.terms-scroll-box { border: 1px solid #e0e0e0; background-color: #f9f9f9; border-radius: 8px; height: 150px; overflow-y: auto; padding: 15px; font-size: 13px; color: #555; line-height: 1.6; margin-bottom: 10px; }
.terms-title { font-weight: 700; color: #333; margin-top: 10px; margin-bottom: 5px; }
.terms-title:first-child { margin-top: 0; }
.terms-list { padding-left: 15px; margin: 5px 0 10px 0; }
.terms-list li { margin-bottom: 3px; }
.agreement-section { display: flex; align-items: center; justify-content: flex-start; margin-top: 10px; }
.agreement-section input[type="checkbox"] { width: 18px; height: 18px; margin-right: 8px; cursor: pointer; }
.agreement-section label { font-size: 14px; color: #333; cursor: pointer; margin: 0; font-weight: 500; }
.cert-input-row { display: flex; gap: 8px; margin-bottom: 8px; }
.cert-input-row input { flex: 1; }
.icon-btn.remove { background: #FFE5E5; border: 1px solid #FFCDCD; color: #D32F2F; border-radius: 8px; width: 45px; cursor: pointer; font-weight: bold; }
.add-btn { width: 100%; padding: 12px; background-color: #f8f9fa; border: 1px dashed #ced4da; color: #868e96; border-radius: 10px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.add-btn:hover { border-color: #FBBF24; color: #F59E0B; background-color: #FFFBEB; }

.counter-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  width: 160px;
  overflow: hidden;
  background-color: white;
}

.counter-btn {
  background-color: #f8f9fa;
  border: none;
  padding: 12px 18px;
  font-size: 18px;
  color: #555;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.counter-btn:hover:not(:disabled) {
  background-color: #e9ecef;
}

.counter-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
  background-color: #f1f3f5;
}

.count-display {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  flex: 1;
  text-align: center;
  user-select: none;
}

.location-btn {
  background-color: #ffffff;
  border: 1px solid #4CAF50;
  color: #4CAF50;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  transition: all 0.2s;
  width: 100%;
}

.location-btn:hover {
  background-color: #e8f5e9;
}

.location-btn:disabled {
  border-color: #ccc;
  color: #999;
  cursor: not-allowed;
  background-color: #f9f9f9;
}

.status-msg {
  font-size: 13px;
  margin-top: 5px;
  font-weight: bold;
}
.status-msg.success { color: #2E7D32; }
.status-msg.error { color: #d32f2f; }
</style>