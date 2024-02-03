import axios from 'axios';

const getUsername = async function (accessToken) {
  try {
    const response = await axios.get('http://localhost:8000/user/get_username', {
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


const likeImage = async function (imageId, accessToken) {
  try {
    const response = await axios.post(`http://localhost:8000/image/like/${imageId}`, null, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.data.success; // Assuming the server responds with success field
  } catch (error) {
    console.error('Error liking image:', error);
    throw error;
  }
};

export { getUsername, likeImage };
