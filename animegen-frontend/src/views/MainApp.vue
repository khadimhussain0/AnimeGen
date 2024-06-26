<template>
  <div class="header">
    <div class="logo"><img src="../assets/animegen.png" alt="AnimeGen" width="64" height="64"
        style="border-radius: 30px; margin-left: 3px;"></div>
    <div class="user-info">
      <span class="credits" @click="console.log('credits')"> 🪙{{ credits }} </span>
      <span class="username">{{ username }}</span>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </div>
  <div class="container">

    <div class="input-section">
      <input v-model="prompt" id="prompt" type="text" placeholder="Enter Text Prompt" class="styled-input"
        autocomplete="off" required>
      <input v-model="negativePrompt" id="negativePrompt" type="text" placeholder="Negative Prompt" class="styled-input"
        autocomplete="off">

      <button @click="generateImages" :disabled="loading" class="generate-button">Generate Images</button>
      <spinner :loading="loading" />
    </div>


    <div class="tab-sections">
      <div :class="tabClasses['community']" @click="switchTab('community')">
        Community Creations
      </div>
      <div :class="tabClasses['my-creations']" @click="switchTab('my-creations')">
        My Creations
      </div>
    </div>
    <div class="image-gallery" v-if="selectedTab === 'community'">
      <!-- Display Images -->
      <div v-for="image in communityImages" :key="image.id" class="gallery-item">
        <div class="image-container">
          <div class="image-wrapper">
            <img :src="image.url" alt="image.id" class="rounded-image">
          </div>
          <!-- Like Button -->
          <button @click="likeImage(image.id)" class="like-button" :class="{ 'liked': likedImages.includes(image.id) }">
            ❤️
          </button>

          <!-- Download Button -->
          <button @click="downloadImage(image.url)" class="download-button">
            <img src="../assets/download-icon.gif" alt="download icon" width="24" height="18" style="border-radius: 5px;">
          </button>
        </div>
      </div>
    </div>

    <div class="image-gallery" v-if="selectedTab === 'my-creations'">
      <!-- Display Images -->
      <div v-for="image in myImages" :key="image.id" class="gallery-item">
        <div class="image-container">
          <div class="image-wrapper">
            <img :src="image.url" alt="image.id" class="rounded-image">
          </div>

          <!-- Like Button -->
          <button @click="likeImage(image.id)" class="like-button">
            ❤️
          </button>

          <!-- Download Button -->
          <button @click="downloadImage(image.url)" class="download-button">
            <img src="../assets/download-icon.gif" alt="download icon" width="24" height="18" style="border-radius: 5px;">
          </button>
        </div>
      </div>
    </div>
  </div>
  <notification-modal :show="showNotification" :message="notificationMessage" :notification-type="notificationType"
    @close="hideNotification" />
</template>

<script>
import NotificationModal from '@/components/NotificationModal.vue';
import Spinner from "@/components/Spinner.vue"
import NotificationMixin from '@/mixins/notificationMixin.js';
import { generateImages, fetchImages } from '../services/image_service';
import { getUsername, getCredits } from '../services/utils';

export default {
  mixins: [NotificationMixin],
  components: {
    Spinner,
  },
  data() {
    return {
      showNotification: false,
      notificationMessage: '',
      notificationType: 'info',
      loading: false,
      prompt: '',
      negativePrompt: '',
      accessToken: localStorage.getItem('accessToken') || '',
      isLoggedIn: Boolean(localStorage.getItem('accessToken')), // Add isLoggedIn variable
      username: '',
      credits: 0,
      selectedTab: 'my-creations',
      likedImages: [],
      tabClasses: {
        community: 'tab1',
        'my-creations': 'tab2',
      },
      communityImages: [],
      myImages: [],
    };
  },
  mounted() {
    this.fetchUsername();
    this.fetchCredits();
    this.fetchCommunityImages();
    this.fetchUserImages();
  },
  methods: {
    async generateImages() {
      if (this.prompt===""){
        console.log("Please add prompt")
        this.showNotificationModal('info', 'Please Enter Text Prompt');
      }else{
      this.loading = true;

      try {
        const newImages = await generateImages(this.accessToken, this.prompt, this.negativePrompt);
        this.myImages = [...newImages, ...this.myImages];
        this.credits = this.fetchCredits()
      } catch (error) {
        console.error("Error generating images:", error);
        if (this.credits<2){
        this.showNotificationModal('info', 'Not Enough Credits');
        }else{
          this.showNotificationModal('info', 'Image Generation Model Under Heavy Load\nTry Again!');
        }
      } finally {
        this.loading = false;
      }
    }},
    async fetchCommunityImages() {
      this.loading = true;

      try {
        const newImages = await fetchImages(this.accessToken, "community");
        this.communityImages = [...newImages, ...this.communityImages];
      } catch (error) {
        console.error("Error Fetching images:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchUserImages() {
      this.loading = true;

      try {
        const newImages = await fetchImages(this.accessToken);
        this.myImages = [...newImages, ...this.myImages];
      } catch (error) {
        console.error("Error Fetching images:", error);
      } finally {
        this.loading = false;
      }
    },
    async likeImage(imageId) {
      try {
        const isSuccess = await likeImage(imageId, this.accessToken);

        if (isSuccess) {
          // Toggle liked state
          this.toggleLiked(imageId);
        }
      } catch (error) {
        // Handle error as needed
      }
    },

    toggleLiked(imageId) {
      const index = this.likedImages.indexOf(imageId);
      if (index === -1) {
        // If not liked, add to likedImages
        this.likedImages.push(imageId);
      } else {
        // If liked, remove from likedImages
        this.likedImages.splice(index, 1);
      }
    },

    isLiked(imageId) {
      return this.likedImages.includes(imageId);
    },

    async downloadImage(imageUrl) {
      try {
        const response = await fetch(imageUrl);
        const blob = await response.blob();

        // Create a link element with download attribute and trigger a click event
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'animegen.png';
        link.click();
      } catch (error) {
        console.error('Error downloading image:', error);
        // Handle error as needed
      }
    },
    switchTab(tab) {
      this.selectedTab = tab;
      Object.keys(this.tabClasses).forEach((key) => {
        this.tabClasses[key] = 'tab2';
      });
      this.tabClasses[tab] = 'tab-selected';
    },
    async fetchUsername() {
      try {
        this.username = await getUsername(this.accessToken);
      } catch (error) {
        console.log(error)
        return "User"
      }
    },
    async fetchCredits() {
      try {
        this.credits = await getCredits(this.accessToken);
      } catch (error) {
        console.log(error)
        return "0"
      }
    },
    logout() {
      localStorage.removeItem('accessToken');
      this.isLoggedIn = false;
      this.$router.push('/auth');
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
  /* padding: 10px; */
  background-color: #1f1f1f;
  /* border-radius: 20px; */
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  font-size: 20px;
  color: #45a049;
  /* margin-right: 10px; */
  background: linear-gradient(90deg, #f441a5, #03a9f4);
  border-top-left-radius: 100px;
  border-bottom-left-radius: 100px;
  padding: 10px;
}

.credits {
  font-size: 18;
  color: #020202;
  /* margin-right: 10px; */
  background: linear-gradient(90deg, #f441a5, #03a9f4);
  border-radius: 50px;
  padding: 10px;
  margin-right: 20px;
}
.logout-button {
  background-color: #d9534f;
  color: white;
  padding: 10px;
  height: 43px;
  width: 80px;
  margin-right: 10px;
  font-size: medium;
  border: none;
  border-top-right-radius: 100px;
  border-bottom-right-radius: 100px;
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
  margin: 10px;
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
  background: linear-gradient(90deg, #f441a5, #03a9f4);
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

.tab1 {
  flex: 1;
  margin: 5px;
  padding: 10px;
  text-align: center;
  background: #454141;
  ;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 30px;
}

.tab2 {
  flex: 1;
  margin: 5px;
  padding: 10px;
  text-align: center;
  background: #454141;
  ;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 30px;
}

.tab-selected {
  flex: 1;
  margin: 5px;
  padding: 10px;
  text-align: center;
  background: linear-gradient(90deg, #27ed09, #06d429);
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 30px;
}


.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.gallery-item {
  flex: 1 0 30%;
}

.image-container {
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.rounded-image {
  border-radius: 10px;
  width: 100%;
  height: auto;
  transition: transform 0.3s ease-in-out;
}

.rounded-image:hover {
  transform: scale(1.1);
  border-radius: 10px;
}

.like-button {
  position: absolute;
  top: 10px;
  right: 50px;
  background: #ffffff;
  border: none;
  border-radius: 50%;
  padding: 5px;
  cursor: pointer;
  font-size: 18px;
  transition: background 0.3s ease-in-out;
}

.download-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #ffffff;
  border: none;
  border-radius: 50%;
  padding: 5px;
  cursor: pointer;
  font-size: 18px;
  transition: background 0.3s ease-in-out;
}

.like-button:hover {
  background: #da1010;
}
.download-button:hover {
  background: #18bb23;
}

.image-wrapper {
  border-radius: 10px;
  overflow: hidden;
}

.liked {
  color: red;
  background-color: red;
  
}

.liked:hover{
  background-color: red;
}
</style>