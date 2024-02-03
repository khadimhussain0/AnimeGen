import axios from 'axios';

const generateImages = async function (accessToken, prompt, negativePrompt) {
  try {
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    const response = await axios.post('http://localhost:8000/generate', {
      prompt,
      negativePrompt,
    }, { headers });

    return response.data.images.map(image => ({
      url: image.url,
      key: image.key,
    }));
  } catch (error) {
    console.error("Error generating images:", error);
    throw error;
  }
};

const fetchCommunityImages = async function (accessToken) {
  try {
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    const response = await axios.get('http://localhost:8000/images/', { headers });

    return response.data.images.map(image => ({
      url: image.url,
      key: image.key,
    }));
  } catch (error) {
    console.error("Error fetching community images:", error);
    throw error;
  }
};

export { generateImages, fetchCommunityImages };
