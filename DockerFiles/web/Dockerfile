FROM node:20-alpine
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

EXPOSE 3000
# node_modules persiste en volumen anónimo; código montado como bind-mount → hot-reload via Vite
CMD ["npm", "run", "dev"]
