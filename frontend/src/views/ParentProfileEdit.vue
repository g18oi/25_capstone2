<template>
  <div class="edit-page">
    <TheHeader />

    <main class="edit-container">
      <div class="edit-card">
        <h2 class="title">학부모 정보 수정</h2>
        
        <form @submit.prevent="updateProfile" class="edit-form">
          
          <div class="profile-image-section">
            <div class="image-wrapper">
              <img :src="profile.image || 'https://via.placeholder.com/150'" alt="프로필 이미지" class="profile-img" />
              <label for="file-upload" class="upload-btn">
                📷
              </label>
              <input type="file" id="file-upload" @change="handleImageChange" accept="image/*" hidden />
            </div>
            <p class="image-hint">프로필 사진을 변경하려면 클릭하세요</p>
          </div>

          <div class="form-group">
            <label for="name">이름</label>
            <input 
              type="text" 
              id="name" 
              v-model="profile.name" 
              placeholder="이름을 입력하세요"
              required 
            />
          </div>

          <div class="form-group">
            <label for="phone">연락처</label>
            <input 
              type="tel" 
              id="phone" 
              v-model="profile.phone" 
              placeholder="010-0000-0000"
              required 
            />
          </div>

          <div class="form-group">
            <label for="address">주소</label>
            <input 
              type="text" 
              id="address" 
              v-model="profile.address" 
              placeholder="주소를 입력하세요"
            />
          </div>

          <div class="form-group">
            <label for="bio">아이/가족 소개</label>
            <textarea 
              id="bio" 
              v-model="profile.bio" 
              placeholder="선생님에게 보여줄 간단한 소개를 적어주세요."
              rows="4"
            ></textarea>
          </div>

          <div class="button-group">
            <button type="button" class="btn-cancel" @click="$router.go(-1)">취소</button>
            <button type="submit" class="btn-save">수정 완료</button>
          </div>

        </form>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import TheHeader from '@/components/TheHeader.vue';

export default {
  name: 'ParentProfileEdit',
  components: { TheHeader },
  data() {
    return {
      profile: {
        name: '',
        phone: '',
        address: '',
        bio: '',
        image: null, // 이미지 URL 또는 base64
        imageFile: null // 실제 업로드할 파일 객체
      }
    };
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem('token');
        // 백엔드 API 주소에 맞게 수정 필요 (예: /api/user/me 또는 /api/parent/me)
        const res = await axios.get('/api/user/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        // 받아온 데이터 매핑
        const data = res.data;
        this.profile.name = data.name;
        this.profile.phone = data.phone || '';
        this.profile.address = data.address || '';
        this.profile.bio = data.bio || ''; 
        // this.profile.image = data.profile_image_url; // 백엔드에 이미지 필드가 있다면
      } catch (error) {
        console.error('정보 로드 실패', error);
        // alert('정보를 불러오는데 실패했습니다.');
      }
    },
    handleImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.profile.imageFile = file;
        // 미리보기 생성
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profile.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        
        // 이미지 파일이 있다면 FormData 사용, 없다면 일반 JSON 전송
        // 여기서는 간단히 JSON 예시로 듭니다. (백엔드 구현에 따라 FormData로 변경 필요)
        const updateData = {
            name: this.profile.name,
            phone: this.profile.phone,
            address: this.profile.address,
            bio: this.profile.bio
        };

        await axios.put('/api/user/me', updateData, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        alert('수정이 완료되었습니다!');
        this.$router.push('/profile'); // 프로필 메인으로 이동
      } catch (error) {
        console.error('수정 실패', error);
        alert('수정 중 오류가 발생했습니다.');
      }
    }
  }
};
</script>

<style scoped>
/* 전체 페이지 배경 */
.edit-page {
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 메인 컨테이너 */
.edit-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

/* 카드 스타일 */
.edit-card {
  background: white;
  width: 100%;
  max-width: 500px;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

/* 프로필 이미지 섹션 */
.profile-image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.image-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
}

.profile-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #eee;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #4a90e2;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  border: 2px solid white;
}

.image-hint {
  font-size: 12px;
  color: #888;
  margin-top: 8px;
}

/* 입력 폼 스타일 */
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #444;
  font-size: 14px;
}

input, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.2s;
  box-sizing: border-box; /* 패딩 포함 너비 계산 */
}

input:focus, textarea:focus {
  border-color: #4a90e2;
  outline: none;
}

textarea {
  resize: vertical;
}

/* 버튼 스타일 */
.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

button {
  flex: 1;
  padding: 14px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  border: none;
}

.btn-cancel {
  background-color: #f1f3f5;
  color: #495057;
}

.btn-cancel:hover {
  background-color: #e9ecef;
}

.btn-save {
  background-color: #4a90e2;
  color: white;
}

.btn-save:hover {
  background-color: #357abd;
}
</style>