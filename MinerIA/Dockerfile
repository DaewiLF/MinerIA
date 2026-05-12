FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Usamos --host para que Vite escuche en todas las interfaces de red del contenedor
CMD ["npm", "run", "dev", "--", "--host"]