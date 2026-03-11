import { createRouter, createWebHistory } from "vue-router";
import { session } from "@/data/session";
import { userResource } from "@/data/user";

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/PageLayout.vue"),
    children: [
      {
        path: "",
        redirect: { name: "Advisories" },
      },
      {
        path: "advisories",
        name: "AdvisoriesRoot",
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
      {
        path: "leaderboard",
        name: "Leaderboard",
        component: () => import("@/pages/Leaderboard.vue"),
        meta: {
          public: true,
        },
      },
      {
        path: "reports",
        name: "ReportsRoot",
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
        path: "inbox",
        name: "Inbox",
        component: () => import("@/pages/Upcoming.vue"),
      },
      {
        path: "rewards",
        name: "Rewards",
        component: () => import("@/pages/Upcoming.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/pages/Login.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/b"),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  let isLoggedIn = session.isLoggedIn;

  try {
    await userResource.promise;
  } catch {
    isLoggedIn = false;
  }

  if (!isLoggedIn && to.name !== "Login" && !to.meta.public) {
    next({ name: "Login" });
  } else if (isLoggedIn && to.name === "Login") {
    next({ name: "Advisories" });
  } else {
    next();
  }
});

export default router;
