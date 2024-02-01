<template>
    <div class="header">
      <div class="logo">Your Logo</div>
      <div class="user-info">
        <span class="username">{{ getUsername() }}</span>
        <button @click="logout" class="logout-button">Logout</button>
      </div>
    </div>
  <div class="container">
    <div class="prompt-content">


      <div class="input-section">
        <label for="prompt" class="label">Prompt:</label>
        <input v-model="prompt" id="prompt" type="text" placeholder="Enter Text Prompt" class="styled-input">

        <label for="negativePrompt" class="label">Negative Prompt:</label>
        <input v-model="negativePrompt" id="negativePrompt" type="text" placeholder="Negative Prompt" class="styled-input">

        <button @click="generateImages" :disabled="loading" class="generate-button">Generate Images</button>
      </div>
    </div>

    <div class="tab-sections">
      <div class="tab" @click="switchTab('community')">Community Creations</div>
      <div class="tab" @click="switchTab('my')">My Creations</div>
    </div>

    <div class="image-gallery" v-if="selectedTab === 'community'">
      <!-- Dummy images, replace with API data -->
      <div v-for="image in communityImages" :key="image.id" class="gallery-item">
        <img :src="image.url" alt="Community Creation" class="gallery-image">
      </div>
    </div>

    <div class="image-gallery" v-if="selectedTab === 'my'">
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
      myImages: [], // Replace with API data
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
      // Implement logout logic here
    },
    getUsername() {
      // Replace with actual username retrieval logic
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
    justify-content: center;
    align-items: center;
    height: 90vh;
    background-color: #0d0a0a;
    margin: 50px;
    border-radius: 20px;
  }

  .prompt-content {
    display: flex;
    flex-direction: column;
    align-items: left;
    margin: 20px;
    color: #ffffff;
    background-color: #1f1c1c;
    padding: 20px;
    border-radius: 10px;
  }

.logout-button:hover {
  background-color: #c9302c;
}

.input-section {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.styled-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #45a049;
  border-radius: 4px;
  margin-bottom: 10px;
  transition: border-color 0.3s;
}

.styled-input:focus {
  border-color: #45a049;
}

.label {
  font-size: 16px;
  color: #ffffff;
  margin-bottom: 5px;
}

.generate-button {
  background-color: #2196F3;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.generate-button:disabled {
  background-color: #ddd;
  color: #555;
  cursor: not-allowed;
}

.generate-button:hover {
  background-color: #0b7dda;
}

.tab-sections {
  display: flex;
  margin-bottom: 10px;
}

.tab {
  flex: 1;
  padding: 10px;
  text-align: center;
  background-color: #1f1c1c;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
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
  flex: 1 0 30%; /* Adjust as needed */
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