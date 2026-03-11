import App from "@/App.vue";
import "@/styles/index.css";
import router from "@/router";
import { createApp } from "vue";
import { setConfig, frappeRequest, resourcesPlugin } from "frappe-ui";
import { useTheme } from "@/composables/useTheme";

setConfig("resourceFetcher", frappeRequest);

useTheme().initTheme();

const app = createApp(App);
app.use(router);
app.use(resourcesPlugin);
app.mount("#app");
