<script setup lang="ts">
import { Sidebar as USidebar } from "frappe-ui";
import BugIcon from "~icons/lucide/bug";
import ChartIcon from "~icons/lucide/trending-up";
import GlobeIcon from "~icons/lucide/globe";
import InboxIcon from "~icons/lucide/inbox";
import MoneyIcon from "~icons/lucide/hand-coins";
import MoonIcon from "~icons/lucide/moon";
import SettingsIcon from "~icons/lucide/settings";
import UserIcon from "~icons/lucide/user";
</script>

<template>
	<USidebar
		disable-collapse
		:header="{
			title: 'Bounty',
			subtitle: 'Sabu Siyad',
			menuItems: [
				{
					label: 'Toggle Theme',
					icon: MoonIcon,
					onClick: () => {},
				},
				{
					label: 'Logout',
					icon: UserIcon,
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
						to: '',
						icon: ChartIcon,
					},
					{
						label: 'Reports',
						to: '',
						icon: BugIcon,
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
