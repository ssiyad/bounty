import { session } from "@/data/session";
import { userResource } from "@/data/user";
import { createRouter, createWebHistory } from "vue-router";

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
				path: "drafts",
				name: "DraftsRoot",
				children: [
					{
						path: "",
						name: "Drafts",
						component: () => import("@/pages/Drafts.vue"),
					},
					{
						path: "draft",
						name: "Draft",
						component: () => import("@/pages/Draft.vue"),
					},
				],
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
				component: () => import("@/pages/Inbox.vue"),
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
	history: createWebHistory("/s"),
	routes,
});

router.beforeEach(async (to, _from, next) => {
	if (to.meta.public || to.name === "Login") {
		return next();
	}

	let isLoggedIn = session.isLoggedIn;

	try {
		await userResource.promise;
	} catch {
		isLoggedIn = false;
	}

	if (!isLoggedIn) {
		window.location.href = "/login";
		return;
	}

	next();
});

export default router;
