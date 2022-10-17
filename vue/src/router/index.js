import { createRouter, createWebHistory } from "vue-router";
import StreamView from "../views/StreamView.vue";
import HomeView from "../views/HomeView.vue";
import MasterLogView from "../views/MasterLogView.vue";


const routes = [
  {
    path: "/",
    name: "overview",
    component: HomeView,
  },
  {
    path: "/master",
    name: "masterlog",
    component: MasterLogView,
  },
  {
    path: "/stream/:id",
    name: "stream",
    component: StreamView,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
