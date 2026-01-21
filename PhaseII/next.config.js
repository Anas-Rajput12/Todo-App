/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: false, // Disable turbo to avoid potential caching issues
  },
  // Disable webpack cache to prevent file locking issues
  webpack: (config, { dev, isServer }) => {
    if (!dev) {
      return config;
    }

    // Disable persistent caching in development
    if (config.cache) {
      delete config.cache;
    }

    return config;
  },
};

module.exports = nextConfig;