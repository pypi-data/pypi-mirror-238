import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import sveltePreprocess from "svelte-preprocess";
// @ts-ignore
import custom_media from "postcss-custom-media";
import global_data from "@csstools/postcss-global-data";
// @ts-ignore
import prefixer from "postcss-prefix-selector";
import { readFileSync } from "fs";
import { resolve } from "path";

const version_path = resolve(__dirname, "../../gradio/package.json");
const theme_token_path = resolve(__dirname, "../theme/src/tokens.css");
const version_raw = JSON.parse(
	readFileSync(version_path, { encoding: "utf-8" })
).version.trim();
const version = version_raw.replace(/\./g, "-");

const client_version_path = resolve(
	__dirname,
	"../../client/python/gradio_client/package.json"
);
const client_version_raw = JSON.parse(
	readFileSync(client_version_path, {
		encoding: "utf-8"
	})
).version.trim();

import {
	inject_ejs,
	patch_dynamic_import,
	generate_cdn_entry,
	generate_dev_entry,
	handle_ce_css,
	inject_component_loader,
	resolve_svelte
} from "./build_plugins";

const GRADIO_VERSION = version || "asd_stub_asd";
const TEST_CDN = !!process.env.TEST_CDN;
const CDN = TEST_CDN
	? "http://localhost:4321/"
	: `https://gradio.s3-us-west-2.amazonaws.com/${version_raw}/`;
const TEST_MODE = process.env.TEST_MODE || "jsdom";

//@ts-ignore
export default defineConfig(({ mode }) => {
	console.log(mode);
	const targets = {
		"production:cdn": "../../gradio/templates/cdn",
		"production:local": "../../gradio/templates/frontend",
		"dev:custom": "../../gradio/templates/frontend"
	};
	const CDN_URL = mode === "production:cdn" ? CDN : "/";
	const production =
		mode === "production:cdn" ||
		mode === "production:local" ||
		mode === "production:website" ||
		mode === "production:lite";
	const is_cdn = mode === "production:cdn" || mode === "production:website";
	const is_lite = mode.endsWith(":lite");

	return {
		base: is_cdn ? CDN_URL : "./",

		server: {
			port: 9876,
			open: is_lite ? "/lite.html" : "/"
		},

		build: {
			sourcemap: true,
			target: "esnext",
			minify: production,
			outDir: is_lite ? resolve(__dirname, "../lite/dist") : targets[mode],
			// To build Gradio-lite as a library, we can't use the library mode
			// like `lib: is_lite && {}`
			// because it inevitably enables inlining of all the static file assets,
			// while we need to disable inlining for the wheel files to pass their URLs to `micropip.install()`.
			// So we build it as an app and only use the bundled JS and CSS files as library assets, ignoring the HTML file.
			// See also `lite.ts` about it.
			rollupOptions: is_lite
				? {
						input: "./lite.html",
						output: {
							// To use it as a library, we don't add the hash to the file name.
							entryFileNames: "lite.js",
							assetFileNames: (file) => {
								if (file.name?.endsWith(".whl")) {
									// Python wheel files must follow the naming rules to be installed, so adding a hash to the name is not allowed.
									return `assets/[name].[ext]`;
								}
								if (file.name === "lite.css") {
									// To use it as a library, we don't add the hash to the file name.
									return `[name].[ext]`;
								} else {
									return `assets/[name]-[hash].[ext]`;
								}
							}
						}
				  }
				: {
						external: ["./svelte/svelte.js"],
						makeAbsoluteExternalsRelative: false
				  }
		},

		define: {
			BUILD_MODE: production ? JSON.stringify("prod") : JSON.stringify("dev"),
			BACKEND_URL: production
				? JSON.stringify("")
				: JSON.stringify("http://localhost:7860/"),
			GRADIO_VERSION: JSON.stringify(version)
		},
		css: {
			postcss: {
				plugins: [
					prefixer({
						prefix: `.gradio-container-${version}`,
						// @ts-ignore
						transform(prefix, selector, prefixedSelector, fileName) {
							if (selector.indexOf("gradio-container") > -1) {
								return prefix;
							} else if (
								selector.indexOf(":root") > -1 ||
								selector.indexOf("dark") > -1 ||
								fileName.indexOf(".svelte") > -1
							) {
								return selector;
							} else if (
								// For the custom element <gradio-lite>. See theme/src/global.css for the details.
								/^gradio-lite(\:[^\:]+)?/.test(selector)
							) {
								return selector;
							}
							return prefixedSelector;
						}
					}),
					custom_media()
				]
			}
		},
		plugins: [
			resolve_svelte(mode === "development"),

			svelte({
				inspector: true,
				compilerOptions: {
					dev: true,
					discloseVersion: false
				},
				hot: !process.env.VITEST && !production,
				preprocess: sveltePreprocess({
					postcss: {
						plugins: [
							global_data({ files: [theme_token_path] }),
							custom_media()
						]
					}
				})
			}),
			generate_dev_entry({ enable: mode !== "development" && mode !== "test" }),
			inject_ejs(),
			patch_dynamic_import({
				mode: is_cdn ? "cdn" : "local",
				gradio_version: GRADIO_VERSION,
				cdn_url: CDN_URL
			}),
			generate_cdn_entry({ enable: is_cdn, cdn_url: CDN_URL }),
			handle_ce_css(),
			inject_component_loader()
		],
		optimizeDeps: {
			exclude: ["@ffmpeg/ffmpeg", "@ffmpeg/util"]
		},
		test: {
			setupFiles: [resolve(__dirname, "../../.config/setup_vite_tests.ts")],
			environment: TEST_MODE,
			include:
				TEST_MODE === "node"
					? ["**/*.node-test.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"]
					: ["**/*.test.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
			exclude: ["**/node_modules/**", "**/gradio/gradio/**"],
			globals: true
		},
		resolve: {
			alias: {
				// For the Wasm app to import the wheel file URLs.
				"gradio.whl": resolve(
					__dirname,
					`../../dist/gradio-${version_raw}-py3-none-any.whl`
				),
				"gradio_client.whl": resolve(
					__dirname,
					`../../client/python/dist/gradio_client-${client_version_raw}-py3-none-any.whl`
				)
			}
		},
		assetsInclude: ["**/*.whl"] // To pass URLs of built wheel files to the Wasm worker.
	};
});
