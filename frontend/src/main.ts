import App from "@/App.vue";
import "@/styles/index.css";
import { useTheme } from "@/composables/useTheme";
import router from "@/router";
import { frappeRequest, resourcesPlugin, setConfig } from "frappe-ui";
import { createApp } from "vue";

setConfig("resourceFetcher", frappeRequest);

useTheme().initTheme();

const app = createApp(App);
app.use(router);
app.use(resourcesPlugin);
app.mount("#app");
