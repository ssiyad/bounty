<script setup lang="ts">
import { useRoute } from "vue-router";
import { createDocumentResource, Sidebar as USidebar } from "frappe-ui";
import BugIcon from "~icons/lucide/bug";
import ChartIcon from "~icons/lucide/trending-up";
import GlobeIcon from "~icons/lucide/globe";
import InboxIcon from "~icons/lucide/inbox";
import MoneyIcon from "~icons/lucide/hand-coins";
import MoonIcon from "~icons/lucide/moon";
import SettingsIcon from "~icons/lucide/settings";
import UserIcon from "~icons/lucide/user";
import { session } from "../data/session";

const route = useRoute();

const user = createDocumentResource({
	doctype: "User",
	name: session.user!,
	cache: ["User", session.user!],
	auto: true,
});

const toggleTheme = () => {
	const currentTheme = document.documentElement.getAttribute("data-theme");
	const newTheme = currentTheme === "dark" ? "light" : "dark";
	document.documentElement.setAttribute("data-theme", newTheme);
};

const isActiveRoute = (name: string) => {
	return route.matched.some((record) => record.name === name);
};
</script>

<template>
	<USidebar
		disable-collapse
		:header="{
			title: 'Bounty',
			subtitle: user.doc?.full_name,
			menuItems: [
				{
					label: 'Toggle Theme',
					icon: MoonIcon,
					onClick: toggleTheme,
				},
				{
					label: 'Logout',
					icon: UserIcon,
					onClick: () => session.logout.submit(),
				},
			],
		}"
		:sections="[
			{
				label: '',
				items: [
					{
						label: 'Inbox',
						to: '',
						icon: InboxIcon,
					},
					{
						label: 'Settings',
						to: '',
						icon: SettingsIcon,
					},
				],
			},
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
						label: 'Reports',
						icon: BugIcon,
						to: {
							name: 'Reports',
						},
						isActive: isActiveRoute('Reports'),
					},
					{
						label: 'Rewards',
						to: '',
						icon: MoneyIcon,
					},
					{
						label: 'Published',
						to: '',
						icon: GlobeIcon,
					},
				],
			},
		]"
	/>
</template>
