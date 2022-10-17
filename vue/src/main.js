import { createApp, VueElement } from "vue";
import { createPinia } from 'pinia';
import App from "./App.vue";
import router from "./router";
import WaveUI from "wave-ui";
import "wave-ui/dist/wave-ui.css";

import "./assets/main.css";

const pinia = createPinia();
const app = createApp(App);

new WaveUI(app, {});

app.use(pinia);
app.use(router);

app.mount("#app");
