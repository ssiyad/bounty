<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { createDocumentResource, Sidebar as USidebar } from "frappe-ui";
import BugIcon from "~icons/lucide/bug";
import ChartIcon from "~icons/lucide/trending-up";
import GlobeIcon from "~icons/lucide/globe";
import InboxIcon from "~icons/lucide/inbox";
import LogoutIcon from "~icons/lucide/log-out";
import MoneyIcon from "~icons/lucide/hand-coins";
import SettingsIcon from "~icons/lucide/settings";
import SunIcon from "~icons/lucide/sun";
import { session } from "../data/session";
import SettingsDialog from "./settings/SettingsDialog.vue";

const route = useRoute();

const user = createDocumentResource({
	doctype: "User",
	name: session.user!,
	cache: ["User", session.user!],
	auto: true,
});

const applyTheme = (theme: string) => {
	document.documentElement.setAttribute("data-theme", theme);
	localStorage.setItem("theme", theme);
};

const toggleTheme = () => {
	const currentTheme = document.documentElement.getAttribute("data-theme");
	const newTheme = currentTheme === "dark" ? "light" : "dark";
	applyTheme(newTheme);
};

onMounted(() => {
	const savedTheme = localStorage.getItem("theme");
	if (savedTheme) {
		applyTheme(savedTheme);
	}
});

const isActiveRoute = (name: string) => {
	return route.matched.some((record) => record.name === name);
};

const isSettingsDialogOpen = ref(false);
</script>

<template>
	<SettingsDialog v-model="isSettingsDialogOpen" />
	<USidebar
		disable-collapse
		:header="{
			title: 'Bounty',
			subtitle: user.doc?.full_name,
			menuItems: [
				{
					label: 'Toggle Theme',
					icon: SunIcon,
					onClick: toggleTheme,
				},
				{
					label: 'Logout',
					icon: LogoutIcon,
					onClick: () => session.logout.submit(),
				},
			],
		}"
		:sections="[
			{
				label: '',
				items: [
					{
						label: 'Leaderboard',
						icon: ChartIcon,
						to: {
							name: 'Leaderboard',
						},
						isActive: isActiveRoute('Leaderboard'),
					},
					{
						label: 'Advisories',
						icon: GlobeIcon,
						to: {
							name: 'Advisories',
						},
						isActive: isActiveRoute('Advisories'),
					},
				],
			},
			{
				label: '',
				items: [
					{
						label: 'Inbox',
						to: '',
						icon: InboxIcon,
						condition: () => session.isLoggedIn,
					},
					{
						label: 'Settings',
						icon: SettingsIcon,
						isActive: isSettingsDialogOpen,
						onClick: () => (isSettingsDialogOpen = true),
						condition: () => session.isLoggedIn,
					},
				].filter((item) => item.condition()),
			},
			{
				label: '',
				items: [
					{
						label: 'Reports',
						icon: BugIcon,
						to: {
							name: 'Reports',
						},
						isActive: isActiveRoute('Reports'),
						condition: () => session.isLoggedIn,
					},
					{
						label: 'Rewards',
						icon: MoneyIcon,
						to: {
							name: 'Rewards',
						},
						isActive: isActiveRoute('Rewards'),
						condition: () => session.isLoggedIn,
					},
				].filter((item) => item.condition()),
			},
		]"
	/>
</template>
