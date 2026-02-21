# STAGE 1: Build
FROM node:20-alpine AS builder
WORKDIR /usr/src/app

# Copy dependency files first to leverage Docker's cache layer
COPY package*.json ./
COPY prisma ./prisma/

# Install ALL dependencies (including dev dependencies for the build)
RUN npm install

# Copy everything else and build the production bundle
COPY . .
ENV DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy"
RUN npx prisma generate
RUN npm run build

# STAGE 2: Run
FROM node:20-alpine AS runner
WORKDIR /usr/src/app

# Only copy what we need to run: node_modules and the compiled dist folder
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/package*.json ./

# Prisma needs the schema file at runtime
COPY --from=builder /usr/src/app/prisma ./prisma

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/src/main.js"]