import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: false,
  experimental: {
    optimizePackageImports: ["@chakra-ui/react","react-icons"],
  },
};

export default nextConfig;
