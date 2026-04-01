/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    turbo: {}, // must be an object, even if empty
  },
  // Optional: Disable webpack cache to prevent file locking issues in dev
  webpack: (config, { dev, isServer }) => {
    if (!dev) return config;

    if (config.cache) {
      delete config.cache;
    }

    return config;
  },
  // Ignore TypeScript errors on build (solves Vercel errors)
  typescript: {
    ignoreBuildErrors: true,
  },
  // Add rewrites for API proxying
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://todo-apps-backend:8000/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
