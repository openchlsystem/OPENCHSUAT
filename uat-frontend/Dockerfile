# Use Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire frontend project
COPY . .

# Expose the frontend port
EXPOSE 5173

# Run the frontend
CMD ["npm", "run", "dev"]
