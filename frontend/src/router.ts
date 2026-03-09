import { session } from "./data/session";
import { userResource } from "./data/user";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@/pages/Home.vue"),
      },
      {
        path: "",
        name: "Inbox",
        component: () => import("@/pages/Upcoming.vue"),
      },
      {
        path: "reports",
        children: [
          {
            path: "",
            name: "Reports",
            component: () => import("@/pages/Reports.vue"),
          },
          {
            path: ":id",
            name: "Report",
            component: () => import("@/pages/Report.vue"),
          },
        ],
      },
      {
        path: "leaderboard",
        name: "Leaderboard",
        component: () => import("@/pages/Leaderboard.vue"),
      },
      {
        path: "rewards",
        name: "Rewards",
        component: () => import("@/pages/Upcoming.vue"),
      },
      {
        path: "advisories",
        meta: {
          public: true,
        },
        children: [
          {
            path: "",
            name: "Advisories",
            component: () => import("@/pages/Advisories.vue"),
          },
          {
            path: ":id",
            name: "Advisory",
            component: () => import("@/pages/Advisory.vue"),
          },
        ],
      },
    ],
  },
  {
    name: "Login",
    path: "/login",
    component: () => import("@/pages/Login.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/b"),
  routes,
});

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn;

  try {
    await userResource.promise;
  } catch (error) {
    isLoggedIn = false;
  }

  if (!isLoggedIn && to.name !== "Login" && !to.meta.public) {
    next({ name: "Login" });
  } else if (isLoggedIn && to.name === "Login") {
    next({ name: "Home" });
  } else next();
});

export default router;
