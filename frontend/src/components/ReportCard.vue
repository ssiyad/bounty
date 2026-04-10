<script setup lang="ts">
import Target from "@/components/Target.vue";
import { statusTheme } from "@/utils/badgeThemes";
import { formatDate } from "date-fns";
import { Badge } from "frappe-ui";

defineProps<{
	report: {
		name: string;
		title: string;
		target: string | null;
		creation: string;
		status: string;
	};
}>();
</script>

<template>
	<RouterLink
		:to="{
			name: 'Report',
			params: {
				id: report.name,
			},
		}"
		class="block"
	>
		<!-- Mobile card layout -->
		<div class="md:hidden p-4 border-b">
			<div class="flex items-start justify-between gap-2 mb-2">
				<div class="font-medium truncate flex-1">{{ report.title }}</div>
				<Badge :label="report.status" :theme="statusTheme(report.status)" />
			</div>
			<div class="flex items-center gap-3 text-sm text-ink-gray-7">
				<Target v-if="report.target" :target="report.target" />
				<span v-else>&mdash;</span>
				<span class="text-ink-gray-4">&mdash;</span>
				<span>{{ formatDate(report.creation, "PPP") }}</span>
			</div>
		</div>
		<!-- Desktop row layout -->
		<div class="hidden md:flex h-12 px-5 py-4 cursor-pointer">
			<div class="grow">{{ report.title }}</div>
			<div class="w-[180px] text-end">
				<Target v-if="report.target" :target="report.target" class="ml-auto mr-0" />
				<span v-else>&mdash;</span>
			</div>
			<div class="w-[200px] text-end">
				{{ formatDate(report.creation, "PPP") }}
			</div>
			<div class="w-[150px] text-end">
				<Badge :label="report.status" :theme="statusTheme(report.status)" />
			</div>
		</div>
	</RouterLink>
</template>