import { Config } from "@remotion/cli/config";

Config.setBrowserExecutable("/usr/bin/chromium");
Config.setChromiumOpenGlRenderer("angle");
Config.setVideoImageFormat("jpeg");
Config.setCodec("h264");
Config.setPixelFormat("yuv420p");
Config.setConcurrency(2);
