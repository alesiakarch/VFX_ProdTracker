# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# windows fix
RUN chmod +x node_modules/.bin/vite
# 
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Expose frontend port linux
# EXPOSE 5173
# expose windows
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# on linux just run podman-compose up --build
# on windows run that and then in another terminal run podman start vfx_prodtracker_frontend:latest
