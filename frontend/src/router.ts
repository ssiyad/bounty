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
        path: "attempts",
        children: [
          {
            path: "",
            name: "Attempts",
            component: () => import("@/pages/Attempts.vue"),
          },
          {
            path: ":id",
            name: "Attempt",
            component: () => import("@/pages/Attempt.vue"),
          },
        ],
        meta: {
          breadcrumb: "Attempts",
        },
      },
      {
        path: "leaderboard",
        name: "Leaderboard",
        component: () => import("@/pages/Leaderboard.vue"),
        meta: {
          breadcrumb: "Leaderboard",
        },
      },
      {
        path: "account",
        name: "Account",
        component: () => import("@/pages/Account.vue"),
        meta: {
          breadcrumb: "Account",
        },
      },
      {
        path: "sherlock",
        children: [
          {
            path: "",
            name: "Sherlock",
            component: () => import("@/pages/Sherlock.vue"),
          },
          {
            path: ":source",
            name: "SherlockSource",
            component: () => import("@/pages/SherlockSource.vue"),
            meta: {
              breadcrumb: (route: any) => route.params.source,
            },
          },
          {
            path: ":source/endpoints",
            name: "SherlockEndpoints",
            component: () => import("@/pages/SherlockSourceEndpoints.vue"),
            meta: {
              breadcrumb: "Endpoints",
            },
          },
          // {
          //   path: "unused-endpoints",
          //   name: "SherlockUnusedEndpoints",
          //   component: () => import("@/pages/SherlockUnusedEndpoints.vue"),
          //   meta: {
          //     breadcrumb: "Unused Endpoints",
          //   },
          // },
        ],
        meta: {
          breadcrumb: "Sherlock",
        },
      },
    ],
    meta: {
      breadcrumb: "Bounty",
    },
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

// router.beforeEach(async (to, from, next) => {
//   let isLoggedIn = session.isLoggedIn;
//
//   try {
//     await userResource.promise;
//   } catch (error) {
//     isLoggedIn = false;
//   }
//
//   if (!isLoggedIn && to.name !== "Login") {
//     next({ name: "Login" });
//   } //
//   else if (isLoggedIn && to.name === "Login") {
//     next({ name: "Home" });
//   } //
//   else next();
// });

export default router;
