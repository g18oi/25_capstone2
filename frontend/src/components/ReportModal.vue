<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-card">
      <h3>🚨 사용자 신고</h3>
      <p>신고 대상: <strong>{{ targetName }}</strong></p>

      <select v-model="reason" class="full-width">
        <option disabled value="">신고 사유를 선택하세요</option>
        <option>욕설/비하 발언</option>
        <option>시간 약속 위반 (노쇼)</option>
        <option>성희롱</option>
        <option>기타</option>
      </select>

      <textarea
        v-model="details"
        placeholder="내용을 입력해주세요"
        rows="4"
        class="full-width"
      ></textarea>

      <!-- 버튼 영역 -->
      <div class="btn-group">
        <button class="btn-cancel" @click="$emit('close')">
          취소
        </button>
        <button class="btn-red" @click="submitReport">
          신고 접수
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['isVisible', 'targetName', 'targetId'],
  data() {
    return {
      reason: '',
      details: ''
    }
  },
  watch: {
    isVisible(val) {
      if (val) {
        this.reason = ''
        this.details = ''
      }
    }
  },
  methods: {
    submitReport() {
      if (!this.reason) {
        alert('사유를 선택해주세요!')
        return
      }

      console.log(
        `신고 대상 ID: ${this.targetId}, 사유: ${this.reason}, 내용: ${this.details}`
      )

      alert(`${this.targetName}님에 대한 신고가 접수되었습니다.`)
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
/* 화면 전체 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;

  display: flex;
  justify-content: center;
  align-items: center;

  background: rgba(0, 0, 0, 0.5);
  z-index: 99999;
}

/* 모달 카드 */
.modal-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 320px;

  max-height: 80vh;
  overflow-y: auto;

  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* 입력 요소 */
.full-width {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 버튼 그룹 */
.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

/* 취소 버튼 */
.btn-cancel {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  border: 1px solid #ddd;
  background: white;
}

/* 신고 접수 버튼 */
.btn-red {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;

  background-color: #ff4d4f;
  color: white;
  border: none;
  font-weight: bold;
}
</style>
