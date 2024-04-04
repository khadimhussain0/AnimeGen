# AnimeGen
![animegen-round](https://github.com/khadimhussain0/AnimeGen/assets/78732305/45ac6ef9-9736-41f8-98cb-c14ab30900c1)

Generate Anime Images with AI -- based on Diffusion Architecture

## Installation
### prerequisites
```
docker
docker compose
A machine with GPU and appropriate cuda drivers
```
1. Clone this repositry
2. In root directory of the project Run
   ```bash
   docker compose up --build
   ```
   or
   
   ```bash
   docker-compose up --build
   ```
It will install all dependencies inlcuding frontend and Database (Postgress)

3. App will be running at
   http://localhost:3000/app
   
4. Swagger Api Docs can be accessed at
   http://127.0.0.1:8000/docs#/


