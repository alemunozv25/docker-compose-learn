# Use a lightweight Node.js base image
FROM node:22-alpine

# Make sure that node directory is setup
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

# Set the working directory inside the container
# WORKDIR /usr/src/app
WORKDIR /home/node/app

# Copy package.json and package-lock.json (or yarn.lock) first to leverage Docker's build cache
# If non-existant use "npm init" for simple set-up.
COPY package*.json ./

# Switch to node user
USER node

# Install application dependencies
RUN npm install

# Copy the rest of the application code
# COPY . .
COPY --chown=node:node . .

# Expose the port your Node.js application listens on
EXPOSE 8199

# Define the executable to run when the container starts
ENTRYPOINT ["node", "node-web-server.js"]