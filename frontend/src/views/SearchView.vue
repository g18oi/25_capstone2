<template>
  <div class="page-wrapper">
    <TheHeader />
    
    <main class="search-container">
      <section class="search-header">
        <h1 class="page-title">선생님 찾기</h1>
        <div class="search-bar-wrapper">
          <input 
            type="text" 
            v-model="keyword" 
            placeholder="활동(영어, 등하원) 또는 지역을 입력하세요"
            @keyup.enter="performSearch"
          />
          <button class="search-btn" @click="performSearch">🔍</button>
        </div>

        <div class="filter-tags">
          <span 
            v-for="tag in recommendTags" 
            :key="tag" 
            class="tag" 
            @click="selectTag(tag)"
          >
            #{{ tag }}
          </span>
        </div>
      </section>

      <section class="results-section">
        <div class="results-header">
          <span class="count">검색 결과 <strong>{{ searchResults.length }}</strong>건</span>
          <select class="sort-select" v-model="sortBy" @change="performSearch">
            <option value="hourly_pay">시급순</option>
            <option value="name">이름순</option>
          </select>
        </div>

        <div v-if="isLoading" class="msg">검색 중입니다...</div>
        <div v-else-if="searchResults.length === 0" class="msg">검색 결과가 없습니다.</div>

        <div v-else class="results-grid">
          <div 
            v-for="teacher in searchResults" 
            :key="teacher.user_id" 
            class="teacher-card"
            @click="$router.push('/teacher/'+teacher.user_id)"
          >
            <div class="card-image">
              <img v-if="teacher.profile_image" :src="teacher.profile_image" class="profile-img" />
              <div v-else class="placeholder-img"></div>
            </div>
            <div class="card-info">
              <div class="info-top">
                <span class="name">{{ teacher.name }}</span>
                <span class="wage">{{ formatPay(teacher.hourly_pay) }}원/시</span>
              </div>
              <p class="region">📍 {{ teacher.regions }}</p>
              <p class="activities">{{ teacher.activities }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { TheHeader },
  data() {
    return {
      keyword: '',
      searchResults: [],
      isLoading: false,
      sortBy: 'hourly_pay',
      recommendTags: ['영어', '등하원', '책읽기', '실내놀이', '미술', '야외활동']
    };
  },
  mounted() {
    this.performSearch(); 
  },
  methods: {
    selectTag(tag) {
      this.keyword = tag;
      this.performSearch();
    },
    async performSearch() {
      this.isLoading = true;
      try {
        // search.py의 search_sitter API 사용
        // keyword가 있으면 activities나 regions에 포함되는지 검색하도록 백엔드에 파라미터 전달
        // 현재 search.py는 activities, regions 파라미터를 따로 받으므로, 간단히 둘 다에 넣어봄
        const params = {
          sort_by: this.sortBy,
          activities: this.keyword || null, 
          // regions: this.keyword || null // 필요 시 주석 해제 (백엔드 로직에 따라 하나만 보내거나 둘 다 보냄)
        };

        const res = await axios.get('/api/search', {
          params,
          headers: { 'ngrok-skip-browser-warning': 'true' }
        });
        this.searchResults = res.data;
      } catch (error) {
        console.error("검색 실패:", error);
      } finally {
        this.isLoading = false;
      }
    },
    formatPay(pay) {
      return pay ? Number(pay).toLocaleString() : '0';
    }
  }
}
</script>

<style scoped>
.page-wrapper {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.search-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.search-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  color: #333;
  margin-bottom: 25px;
}

.search-bar-wrapper {
  position: relative;
  max-width: 600px;
  margin: 0 auto 20px;
  background-color: white;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  padding: 5px 10px;
  display: flex;
  align-items: center;
}

.search-bar-wrapper input {
  flex: 1;
  border: none;
  padding: 15px 20px;
  font-size: 16px;
  background: transparent;
  outline: none;
}

.search-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 10px 15px;
  border-radius: 50%;
  transition: background 0.2s;
}
.search-btn:hover {
  background-color: #f1f3f5;
}

.filter-tags {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.tag {
  background-color: white;
  border: 1px solid #e9ecef;
  padding: 8px 16px;
  border-radius: 20px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.tag:hover {
  border-color: #FBBF24;
  color: #F59E0B;
  background-color: #FFFBEB;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.count {
  font-size: 16px;
  color: #333;
}
.count strong {
  color: #F59E0B;
}

.sort-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}


.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.teacher-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.teacher-card {
  background-color: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.teacher-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.card-image {
  height: 180px;
  background-color: #f1f3f5;
}

.placeholder-img {
  width: 100%;
  height: 100%;
  background-color: #e9ecef;
}

.card-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.name {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.rating {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.location {
  font-size: 14px;
  color: #888;
  margin-bottom: 12px;
}

.tags {
  margin-bottom: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.hash-tag {
  font-size: 12px;
  color: #666;
  background-color: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
}

.wage {
  margin-top: auto;
  font-size: 16px;
  font-weight: 700;
  color: #F59E0B;
  text-align: right;
}


.no-result {
  text-align: center;
  padding: 80px 0;
  color: #888;
}
.no-result .icon {
  font-size: 48px;
  margin-bottom: 15px;
}
.no-result p {
  line-height: 1.6;
}

@media (max-width: 600px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>