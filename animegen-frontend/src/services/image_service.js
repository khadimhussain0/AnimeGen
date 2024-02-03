function processResponse(response) {
    try {
      if (!response || !response.images || !Array.isArray(response.images)) {
        throw new Error("Invalid response format");
      }
  
      const baseUrl = "http://localhost:8000/images/api/v1/";
  
      return response.images.map((image) => ({
        filename: `${baseUrl}${image.filename}`,
        key: image.key,
      }));
    } catch (error) {
      console.error("Error processing response:", error.message);
      return [];
    }
  }
  
  const someresponse = {
    "message": "success",
    "images": [
      {
        "filename": "image.png",
        "key": 1
      },
      {
        "filename": "image2.png",
        "key": 2
      }
    ]
  };
  
  const processedResponse = processResponse(someresponse);
  console.log(processedResponse);
