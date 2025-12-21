<template>
  <div>
    <TheHeader />
    <main class="page-container">
      <h1>고객센터</h1>
      <div class="content-box">
        <p class="info-text">
          문의사항이 있으시면 아래 연락처로 연락주세요.<br>
          평일 09:00 ~ 18:00 (주말 및 공휴일 휴무)
        </p>
        <div class="contact-info">
          <p>📞 전화: 1588-1818</p>
          <p>📧 이메일: help@ilink.com</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { TheHeader }
}
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 50px 20px;
  text-align: center;
}
h1 {
  margin-bottom: 30px;
  color: #333;
}
.content-box {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.info-text {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 30px;
}
.contact-info p {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 10px 0;
}
</style>