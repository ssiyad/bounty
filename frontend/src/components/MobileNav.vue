<script setup lang="ts">
import { session } from "@/data/session";
import { createResource } from "frappe-ui";
import { useRoute } from "vue-router";
import BugIcon from "~icons/lucide/bug";
import GlobeIcon from "~icons/lucide/globe";
import InboxIcon from "~icons/lucide/inbox";
import DraftIcon from "~icons/lucide/scroll-text";
import ChartIcon from "~icons/lucide/trending-up";

const route = useRoute();

const unreadNotificationCount = createResource({
	url: "security.api.inbox.unread_count",
	auto: session.isLoggedIn,
});

const isActiveRoute = (name: string) => {
	return route.matched.some((record) => record.name === name);
};
</script>

<template>
	<nav class="fixed bottom-0 left-0 right-0 h-12 bg-surface-card border-t flex items-center justify-around px-2 z-50">
		<RouterLink
			v-for="item in [
				{ label: 'Inbox', icon: InboxIcon, to: { name: 'Inbox' }, active: isActiveRoute('Inbox'), badge: unreadNotificationCount.data },
				{ label: 'Leaderboard', icon: ChartIcon, to: { name: 'Leaderboard' }, active: isActiveRoute('Leaderboard') },
				{ label: 'Advisories', icon: GlobeIcon, to: { name: 'Advisories' }, active: isActiveRoute('AdvisoriesRoot') },
				{ label: 'Reports', icon: BugIcon, to: { name: 'Reports' }, active: isActiveRoute('ReportsRoot') },
				{ label: 'Drafts', icon: DraftIcon, to: { name: 'Drafts' }, active: isActiveRoute('DraftsRoot') },
			]"
			:key="item.label"
			:to="item.to"
			class="flex flex-col items-center justify-center py-2 px-3 min-w-[60px] rounded-md transition-colors"
			:class="item.active ? 'text-ink-blue-5 font-semibold' : 'text-ink-gray-4 hover:text-ink-gray-6'"
		>
			<div class="relative">
				<component :is="item.icon" class="w-6 h-6" />
				<span
					v-if="item.badge"
					class="absolute -top-1 -right-1 min-w-[18px] h-[18px] text-[10px] font-medium bg-red-6 text-white rounded-full flex items-center justify-center px-1"
				>
					{{ item.badge > 99 ? '99+' : item.badge }}
				</span>
			</div>
		</RouterLink>
	</nav>
</template>