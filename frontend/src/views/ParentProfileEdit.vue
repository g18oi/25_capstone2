<template>
  <div class="form-page-container">
    <div class="form-card">
      <header class="form-header primary-bg">
        <h1>학부모 정보 수정</h1>
      </header>

      <form @submit.prevent="handleUpdate" class="form-body">
        <div class="form-group">
          <label>이름</label>
          <input type="text" v-model="form.name" required />
        </div>

        <div class="form-group">
          <label>연락처</label>
          <input type="tel" v-model="form.contact" />
        </div>

        <div class="form-group">
          <label>주소</label>
          <input type="text" v-model="form.address" />
        </div>

        <button type="submit" class="btn-primary full-width">
          수정 완료
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        contact: '',
        address: ''
      }
    }
  },

  mounted() {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true'
    if (!isLoggedIn) {
      this.$router.push('/login')
      return
    }

    try {
      const userData = sessionStorage.getItem('user')
      if (userData) {
        const user = JSON.parse(userData)
        this.form = {
          name: user.name || '',
          contact: user.contact || '',
          address: user.address || ''
        }
      }
    } catch (e) {
      console.error('사용자 정보 로딩 실패:', e)
    }
  },

  methods: {
    handleUpdate() {
      // 수정된 정보 저장
      sessionStorage.setItem('user', JSON.stringify(this.form))
      sessionStorage.setItem('userName', this.form.name)

      alert('학부모 정보가 수정되었습니다.')
      this.$router.push('/home')
    }
  }
}
</script>

<style scoped>
</style>
