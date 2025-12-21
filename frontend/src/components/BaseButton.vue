<template>
  <button :class="['base-button', type]" @click="$emit('click')">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'BaseButton',
  props: {
    type: {
      type: String,
      default: 'primary'
    }
  }
}
</script>

<style scoped>
.base-button {
  width: 100%;
  padding: 14px 20px;
  border: none;
  border-radius: 10px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 15px;
  transition: all 0.25s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}


.base-button.primary {
  background-color: #FBBF24;
  color: white;
}

.base-button.primary:hover {
  background-color: #F59E0B;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}


.base-button.secondary {
  background-color: #FBBF24;
  color: white;
}

.base-button.secondary:hover {
  background-color: #F59E0B;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}


/* Outline 버튼 (노란색 테두리) */
.base-button.outline {
  background-color: transparent;
  color: #FBBF24;
  border: 2px solid #FBBF24;
  box-shadow: none;
}

.base-button.outline:hover {
  background-color: #FFFBEB;
  color: #F59E0B;
  border-color: #F59E0B;
  transform: translateY(-2px);
}

.base-button:disabled {
  background-color: #e0e0e0;
  color: #a0a0a0;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}
</style>