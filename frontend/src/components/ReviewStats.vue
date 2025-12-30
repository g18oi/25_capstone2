<template>
  <section class="review-stats">
    <h3 class="title">⭐ 학부모 후기 평가</h3>

    <!-- 후기 수치화 -->
    <div
      v-for="item in statList"
      :key="item.key"
      class="stat-row"
    >
      <div class="label">{{ item.label }}</div>

      <div class="bar-wrapper">
        <div class="bar-bg">
          <div
            class="bar-fill"
            :style="{ width: scorePercent(item.value) + '%' }"
          ></div>
        </div>
        <div class="score">
          {{ item.value.toFixed(1) }} / 5
        </div>
      </div>
    </div>

    <!-- 재매칭 확률 -->
    <div v-if="rematchProbability !== null" class="rematch-box">
      <h4>🔁 재매칭 확률</h4>

      <div class="rematch-percent">
        {{ rematchProbability }}%
      </div>

      <div class="bar-bg large">
        <div
          class="bar-fill rematch"
          :style="{ width: rematchProbability + '%' }"
        ></div>
      </div>

      <p class="desc">
        이전 후기 및 활동 이력을 기반으로 계산된 지표입니다.
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ReviewStats',

  props: {
    stats: {
      type: Object,
      required: true
    },
    rematchProbability: {
      type: Number,
      default: null
    }
  },

  computed: {
    statList() {
      return [
        { key: 'tp', label: '시간 약속', value: this.stats.avg_time_punctuality || 0 },
        { key: 'pa', label: '활동 준비성', value: this.stats.avg_preparedness_activity || 0 },
        { key: 'cc', label: '아이와의 소통', value: this.stats.avg_communication_with_child || 0 },
        { key: 'sm', label: '안전 관리', value: this.stats.avg_safety_management || 0 },
        { key: 'cs', label: '보호자 소통', value: this.stats.avg_communication_skill || 0 }
      ]
    }
  },

  methods: {
    scorePercent(score) {
      return Math.min(Math.max((score / 5) * 100, 0), 100)
    }
  }
}
</script>

<style scoped>
.review-stats {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  margin-bottom: 25px;
}

.title {
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 25px;
}

.stat-row {
  margin-bottom: 18px;
}

.label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #555;
}

.bar-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bar-bg {
  flex: 1;
  height: 10px;
  background: #f1f3f5;
  border-radius: 10px;
  overflow: hidden;
}

.bar-bg.large {
  height: 14px;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #FBBF24, #F59E0B);
  border-radius: 10px;
}

.bar-fill.rematch {
  background: linear-gradient(90deg, #4CAF50, #81C784);
}

.score {
  min-width: 70px;
  text-align: right;
  font-size: 13px;
  font-weight: 700;
}

.rematch-box {
  margin-top: 35px;
  padding-top: 25px;
  border-top: 1px solid #eee;
  text-align: center;
}

.rematch-box h4 {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 12px;
}

.rematch-percent {
  font-size: 32px;
  font-weight: 900;
  color: #2E7D32;
  margin-bottom: 12px;
}

.desc {
  margin-top: 8px;
  font-size: 13px;
  color: #888;
}
</style>