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
            placeholder="지역, 활동 내용, 선생님 이름을 검색해보세요"
            @keyup.enter="performSearch"
          />
          <button class="search-btn" @click="performSearch">🔍</button>
        </div>

        <div class="filter-tags">
          <span 
            v-for="tag in recommendTags" 
            :key="tag" 
            class="tag" 
            @click="keyword = tag; performSearch()"
          >
            #{{ tag }}
          </span>
        </div>
      </section>

      <section class="results-section">
        <div class="results-header">
          <span class="count">검색 결과 <strong>{{ filteredList.length }}</strong>건</span>
          <select class="sort-select">
            <option>추천순</option>
            <option>인기순</option>
            <option>최신순</option>
          </select>
        </div>

        <div v-if="filteredList.length > 0" class="results-grid">
          <router-link 
            v-for="teacher in filteredList" 
            :key="teacher.id" 
            :to="'/teacher/' + teacher.id"
            class="teacher-card-link"
          >
            <div class="teacher-card">
              <div class="card-image">
                <div class="placeholder-img"></div>
              </div>
              <div class="card-info">
                <div class="info-top">
                  <span class="name">{{ teacher.name }} 선생님</span>
                  <span class="rating">⭐ {{ teacher.rating }}</span>
                </div>
                <p class="location">📍 {{ teacher.location }}</p>
                <div class="tags">
                  <span v-for="t in teacher.tags" :key="t" class="hash-tag">{{ t }}</span>
                </div>
                <p class="wage">{{ teacher.wage.toLocaleString() }}원 / 시</p>
              </div>
            </div>
          </router-link>
        </div>

        <div v-else class="no-result">
          <div class="icon">😢</div>
          <p>검색 결과가 없습니다.<br>다른 키워드로 검색해보세요.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import TheHeader from '../components/TheHeader.vue';

export default {
  components: { TheHeader },
  data() {
    return {
      keyword: '',
      recommendTags: ['등하원', '영어놀이', '미술', '강남구', '신생아'],
      
      allTeachers: [
        { id: 1, name: '김선생님', location: '서울 강남구', rating: 4.8, wage: 15000, tags: ['#실내놀이', '#영어'] },
        { id: 2, name: '이선생님', location: '서울 서초구', rating: 4.9, wage: 14000, tags: ['#등하원', '#책읽기'] },
        { id: 3, name: '박선생님', location: '경기 성남시', rating: 4.5, wage: 13000, tags: ['#학습지도', '#한글'] },
        { id: 4, name: '최선생님', location: '서울 송파구', rating: 5.0, wage: 16000, tags: ['#야외활동', '#미술'] },
        { id: 5, name: '정선생님', location: '서울 마포구', rating: 4.7, wage: 15000, tags: ['#신생아', '#실내놀이'] },
        { id: 6, name: '강선생님', location: '서울 강동구', rating: 4.6, wage: 13500, tags: ['#등하원', '#영어놀이'] },
      ],
      filteredList: []
    };
  },
  created() {
    this.filteredList = this.allTeachers;
  },
  methods: {
    performSearch() {
      if (!this.keyword.trim()) {
        this.filteredList = this.allTeachers;
        return;
      }
      
      const term = this.keyword.trim();
      this.filteredList = this.allTeachers.filter(t => 
        t.name.includes(term) || 
        t.location.includes(term) ||
        t.tags.some(tag => tag.includes(term))
      );
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