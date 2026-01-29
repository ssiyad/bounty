<script setup lang="ts">
import { formatDate } from "date-fns";
import { useRouter } from "vue-router";
import { Badge, createListResource, usePageMeta } from "frappe-ui";
import { statusTheme } from "../utils/badgeThemes";
import { pageTitle } from "../utils/page";

const router = useRouter();

const attemptsResource = createListResource({
	doctype: "Bounty Attempt",
	cache: ["Attempts"],
	fields: ["name", "title", "creation", "status"],
	pageLength: 99999,
	auto: true,
});

usePageMeta(() => ({
	title: pageTitle("Attempts"),
}));
</script>

<template>
	<div class="container mx-auto py-16">
		<div class="divide-y">
			<div class="flex pb-4 font-medium">
				<div class="w-1/2">Title</div>
				<div class="w-1/4 text-end">Date</div>
				<div class="w-1/4 text-end">Status</div>
			</div>
			<div
				v-for="attempt in attemptsResource.data"
				:key="attempt.name"
				class="flex py-4 cursor-pointer"
				@click="router.push({ name: 'Attempt', params: { id: attempt.name } })"
			>
				<div class="w-1/2">{{ attempt.title }}</div>
				<div class="w-1/4 text-end">{{ formatDate(attempt.creation, "PPP") }}</div>
				<div class="w-1/4 text-end">
					<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
				</div>
			</div>
		</div>
	</div>
</template>
