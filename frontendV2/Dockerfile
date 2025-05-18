# Use a lightweight Node.js image
FROM node:18-alpine

# Set working directory inside the container
WORKDIR /app

# Copy dependency files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire frontend project
COPY . .

# Build the frontend
RUN npm run build

# Serve the built files using a lightweight server
CMD ["npx", "serve", "-s", "dist", "-l", "5174"]


