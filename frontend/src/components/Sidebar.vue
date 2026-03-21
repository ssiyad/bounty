<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { createDocumentResource, Sidebar as USidebar } from "frappe-ui";
import BugIcon from "~icons/lucide/bug";
import ChartIcon from "~icons/lucide/trending-up";
import DraftIcon from "~icons/lucide/scroll-text";
import GlobeIcon from "~icons/lucide/globe";
import InboxIcon from "~icons/lucide/inbox";
import LogoutIcon from "~icons/lucide/log-out";
import MoneyIcon from "~icons/lucide/hand-coins";
import SettingsIcon from "~icons/lucide/settings";
import { session } from "@/data/session";
import SettingsDialog from "@/components/settings/SettingsDialog.vue";

const route = useRoute();

const user = createDocumentResource({
	doctype: "User",
	name: session.user!,
	cache: ["User", session.user!],
	auto: true,
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
			title: 'Security',
			subtitle: user?.doc?.full_name || 'Guest',
			menuItems: [
				{
					label: 'Logout',
					icon: LogoutIcon,
					onClick: () => session.logout.submit(),
					condition: () => session.isLoggedIn,
				},
			].filter((item) => item.condition()),
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
						isActive: isActiveRoute('AdvisoriesRoot'),
					},
				],
			},
			{
				label: '',
				items: [
					{
						label: 'Inbox',
						icon: InboxIcon,
						to: {
							name: 'Inbox',
						},
						isActive: isActiveRoute('Inbox'),
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
						isActive: isActiveRoute('ReportsRoot'),
						condition: () => session.isLoggedIn,
					},
					{
						label: 'Drafts',
						icon: DraftIcon,
						to: {
							name: 'Drafts',
						},
						isActive: isActiveRoute('DraftsRoot'),
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
