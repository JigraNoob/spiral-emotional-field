/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    // Modern experimental features can be enabled here
  },
  webpack: (config) => {
    // Add file-loader for JSONL files
    config.module.rules.push({
      test: /\.(jsonl)$/i,
      type: 'asset/source',
    });
    return config;
  },
  // Enable server components
  experimental: {
    serverComponents: true,
  },
};

// Conditionally enable Turbopack in development
if (process.env.NODE_ENV === 'development') {
  nextConfig.experimental.turbo = {
    rules: {
      // Configure any Turbopack rules here
    }
  };
}

module.exports = nextConfig;
