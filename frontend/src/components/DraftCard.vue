<script setup lang="ts">
import { formatDate } from "date-fns";

defineProps<{
	draft: {
		name: string;
		title: string;
		modified: string;
	};
}>();
</script>

<template>
	<RouterLink
		:to="{
			name: 'Draft',
			query: {
				id: draft.name,
			},
		}"
		class="block"
	>
		<!-- Mobile card layout -->
		<div class="md:hidden p-4 border-b">
			<div class="font-medium truncate">{{ draft.title || 'Untitled' }}</div>
			<div class="text-sm text-ink-gray-7 mt-1">
				{{ formatDate(draft.modified, "PPP") }}
			</div>
		</div>
		<!-- Desktop row layout -->
		<div class="hidden md:flex h-12 px-5 py-4 cursor-pointer">
			<div class="grow">{{ draft.title }}</div>
			<div class="w-[150px] text-end">
				{{ formatDate(draft.modified, "PPP") }}
			</div>
		</div>
	</RouterLink>
</template>