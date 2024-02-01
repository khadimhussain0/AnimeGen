<template>
  <div class="container">
    <div class="prompt-content">
      <div class="input-section">
        <label for="prompt" class="label">Prompt:</label>
        <input v-model="prompt" id="prompt" type="text" placeholder="Enter Text Prompt" class="styled-input">

        <label for="negativePrompt" class="label">Negative Prompt:</label>
        <input v-model="negativePrompt" id="negativePrompt" type="text" placeholder="Negative Prompt" class="styled-input">
        </div>
        <button @click="generateImages" :disabled="loading" class="generate-button">Generate Images</button>
      </div>

    </div>
    <div class="image-container">
      <img ref="generatedImage" alt="Generated Image" class="generated-image">
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
    toggleCustomize() {
      this.isCustomizing = !this.isCustomizing;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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
}

.input-section input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.label {
  align-items: left;
  font-size: 20px;
  width: 100%;
  display: flex;
}

.styled-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #4CAF50;
  border-radius: 4px;
  transition: border-color 0.3s;
}

.styled-input:focus {
  border-color: #45a049;
}

.image-container {
  max-width: 400px;
  margin: auto;
  margin-left: 20px;
}

.generated-image {
  max-width: 100%;
  transition: transform 0.3s;
}

.generated-image:hover {
  transform: scale(1.1);
}

.generate-button {
  background-color: #2196F3;
  color: white;
  padding: 10px 15px;
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
</style>
