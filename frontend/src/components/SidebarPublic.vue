<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { Sidebar as USidebar } from "frappe-ui";
import ChartIcon from "~icons/lucide/trending-up";
import DashboardIcon from "~icons/lucide/layout-grid";
import GlobeIcon from "~icons/lucide/globe";

const route = useRoute();

const applyTheme = (theme: string) => {
	document.documentElement.setAttribute("data-theme", theme);
	localStorage.setItem("theme", theme);
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
						label: 'Dashboard',
						icon: DashboardIcon,
						to: {
							name: 'Reports',
						},
						isActive: isActiveRoute('Reports'),
					},
				],
			},
		]"
	/>
</template>
