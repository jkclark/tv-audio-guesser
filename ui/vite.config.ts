import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/tv-audio-guesser/",
  server: {
    host: "127.0.0.1",
    port: 3000,
  },
});
