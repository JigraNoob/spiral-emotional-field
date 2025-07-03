/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  // Allow reading from the spiral directory
  webpack: (config, { isServer }) => {
    // Add file-loader for JSONL files
    config.module.rules.push({
      test: /\.(jsonl)$/i,
      type: 'asset/source',
    });

    return config;
  },
};

module.exports = nextConfig;
