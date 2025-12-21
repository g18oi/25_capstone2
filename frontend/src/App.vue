<template>
  <router-view @show-modal="showModal"></router-view>
  
  <GlobalModal 
    :visible="isModalVisible" 
    :message="modalMessage" 
    @close="closeModal" 
    @confirm="confirmModal" 
  />
</template>

<script>
import GlobalModal from './components/GlobalModal.vue';

export default {
  name: 'App',
  components: { GlobalModal },
  data() {
    return {
      isModalVisible: false,
      modalMessage: '',
      onConfirm: null,
    }
  },
  methods: {
    showModal({ message, onConfirm }) {
      this.modalMessage = message;
      this.isModalVisible = true;
      this.onConfirm = onConfirm; 
    },
    closeModal() {
      this.isModalVisible = false;
      this.onConfirm = null;
    },
    confirmModal() {
      if (this.onConfirm) {
        this.onConfirm();
      }
      this.closeModal();
    }
  }
}
</script>