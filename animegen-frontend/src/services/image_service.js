import axios from 'axios';
import { orgin } from '@/services/config';

const generateImages = async function (accessToken, prompt, negativePrompt) {
  try {
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    const response = await axios.post(`${orgin}/generate`, {
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

const fetchImages = async function (accessToken, audience='') {
  try {
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    if (audience==='community'){
    const response = await axios.get(`${orgin}/images/community`, { headers });
    return response.data.images.map(image => ({
      url: image.url,
      key: image.key,
    }));
    }else{
      const response = await axios.get(`${orgin}/images/`, { headers });
      return response.data.images.map(image => ({
        url: image.url,
        key: image.key,
      }));
    }
  } catch (error) {
    console.error("Error fetching community images:", error);
    throw error;
  }
};

export { generateImages, fetchImages };
