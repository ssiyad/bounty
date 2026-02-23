<script setup lang="ts">
import { createResource, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const source = route.params.source as string;

usePageMeta(() => ({
	title: pageTitle("Source"),
}));

const overview = createResource({
	url: "bounty.sherlock.api.source.overview",
	auto: true,
	makeParams: () => ({
		source,
	}),
});

const cards = computed(() => [
	{
		title: "Commits",
		value: overview.data?.commit_count || 0,
	},
	{
		title: "Functions",
		value: overview.data?.function_count || 0,
	},
	{
		title: "Endpoints",
		value: overview.data?.endpoint_count || 0,
	},
]);
</script>

<template>
	<div class="overflow-y-auto">
		<div class="grid grid-cols-3 gap-4 p-4">
			<div v-for="card in cards" class="p-4 border rounded space-y-4">
				<p class="font-semibold text-lg">{{ card.title }}</p>
				<p class="text-[96px] font-semibold text-ink-gray-8 text-end">
					{{ card.value.toLocaleString() }}
				</p>
			</div>
		</div>
	</div>
</template>
