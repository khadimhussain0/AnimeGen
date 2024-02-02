<template>
    <div class="header">
      <div class="logo">Your Logo</div>
      <div class="user-info">
        <span class="username">{{ getUsername() }}</span>
        <button @click="logout" class="logout-button">Logout</button>
      </div>
    </div>
  <div class="container">



      <div class="input-section">
        <input v-model="prompt" id="prompt" type="text" placeholder="Enter Text Prompt" class="styled-input">
        <input v-model="negativePrompt" id="negativePrompt" type="text" placeholder="Negative Prompt" class="styled-input">

        <button @click="generateImages" :disabled="loading" class="generate-button">Generate Images</button>
      </div>


    <div class="tab-sections">
      <div class="tab" @click="switchTab('community')">Community Creations</div>
      <div class="tab" @click="switchTab('my-creations')">My Creations</div>
    </div>

    <div class="image-gallery" v-if="selectedTab === 'community'">
      <!-- Dummy images, replace with API data -->
      <div v-for="image in communityImages" :key="image.id" class="gallery-item">
        <img :src="image.url" alt="Community Creation" class="gallery-image">
      </div>
    </div>

    <div class="image-gallery" v-if="selectedTab === 'my-creations'">
      <!-- Dummy images, replace with API data -->
      <div v-for="image in myImages" :key="image.id" class="gallery-item">
        <img :src="image.url" alt="My Creation" class="gallery-image">
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: false,
      prompt: '',
      negativePrompt: '',
      accessToken: localStorage.getItem('accessToken') || '',
      selectedTab: 'community',
      communityImages: [], // Replace with API data
      myImages: [{"url":"https://picsum.photos/500/300", "key":2,"url":"https://picsum.photos/500/300", "key":1}], // Replace with API data
    };
  },
  computed: {
    customizeButtonText() {
      return this.isCustomizing ? 'Hide Customization' : 'Customize';
    },
  },
  methods: {
    async generateImages() {
      this.loading = true;

      try {
        const headers = {
          Authorization: `Bearer ${this.accessToken}`,
        };
        const response = await axios.post('http://localhost:8000/generate', {
          prompt: this.prompt,
          negativePrompt: this.negativePrompt,
        }, { headers, responseType: 'arraybuffer' });

        if (this.$refs.generatedImage) {
          this.$refs.generatedImage.src = URL.createObjectURL(new Blob([response.data]));
        }

      } catch (error) {
        console.error("Error generating images:", error);
      } finally {
        this.loading = false;
      }
    },
    switchTab(tab) {
      this.selectedTab = tab;
    },
    logout() {
    },
    getUsername() {
      return 'JohnDoe';
    },
  },
};
</script>

<style scoped>
  body {
    margin: 0;
    font-family: 'Arial', sans-serif;
    background-color: #101010;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #1f1f1f;
  }

  .user-info {
    display: flex;
    align-items: center;
  }

  .username {
    font-size: 18px;
    color: #45a049;
    margin-right: 10px;
  }

  .logout-button {
    background-color: #d9534f;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .logout-button:hover {
    background-color: #c9302c;
  }

  .container {
    display: flex;
    flex-direction: column; 
    align-items: center; 
    background-color: #0f0d10;
    margin: 50px;
    border-radius: 20px;
  }

  .input-section {
    margin-left: 200px;
    margin-right: 200px;

  }
  .styled-input {
  width: 100%;
  padding: 12px;
  color: white;
  border: none;
  font-size: 15px;
  background: linear-gradient(90deg,#f441a5, #03a9f4);
  border-radius: 40px;
  margin-top: 10px;
  margin-bottom: 10px;
  transition: border-color 0.3s;
}

.styled-input::placeholder {
  color: white;
}

.styled-input:focus {
  border-color: #000000;
}

.generate-button {
  background-color: #2196F3;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 50px;
  height: 50px;
  width: 150px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 15px;
  background: linear-gradient(90deg, #f441a5, #03a9f4);
}

.generate-button:disabled {
  background-color: #ddd;
  color: #555;
  cursor: not-allowed;
}

  .tab-sections {
    display: flex;
    justify-content: center;
    margin-top: 10px;
    width: 99%;
    padding: 10px;
    margin: 10px;
  }

  .tab {
    flex: 1;
    margin: 5px;
    padding: 10px;
    text-align: center;
    background-color: #1f1c1c;
    color: #ffffff;
    cursor: pointer;
    transition: background-color 0.3s;
    border-radius: 30px;
  }

  .tab:hover {
    background-color: #454141;
  }


.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.gallery-item {
  flex: 1 0 30%;
}

.gallery-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  transition: transform 0.3s;
}

.gallery-image:hover {
  transform: scale(1.05);
}
</style>