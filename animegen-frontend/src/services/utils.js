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
  } finally{
    return "   "
  }
};

export { getUsername };
