# Use an official Node runtime as a base image
FROM node:20.11-alpine
# Set the working directory
WORKDIR /usr/src/app

COPY package.json ./
# Install app dependencies
RUN npm install

COPY . .

# Build the React app
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
