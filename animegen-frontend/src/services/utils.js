import axios from 'axios';
import { orgin } from '@/services/config';

const getUsername = async function (accessToken) {
  try {
    const response = await axios.get(`${orgin}/user/get_username`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    const fullName = `${response.data.firstname} ${response.data.lastname}`;
    return fullName;
  } catch (error) {
    console.error('Error during fetching username:', error.message);
    throw error;
  }
};

const getCredits = async function (accessToken) {
  try {
    const response = await axios.get(`${orgin}/credits/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data.credits;
  } catch (error) {
    console.error('Error during fetching credits:', error.message);
    throw error;
  }
};

const likeImage = async function (imageId, accessToken) {
  try {
    const response = await axios.post(`${orgin}/image/like/${imageId}`, null, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.data.success;
  } catch (error) {
    console.error('Error liking image:', error);
    throw error;
  }
};

export { getUsername, getCredits, likeImage };
