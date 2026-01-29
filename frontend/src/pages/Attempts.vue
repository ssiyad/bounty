<script setup lang="ts">
import { Badge, usePageMeta } from "frappe-ui";
import { statusTheme } from "../utils/badgeThemes";
import { pageTitle } from "../utils/page";

const attempts = [
	{ title: "Attempt 1", status: "Pending", date: "2024-06-01" },
	{ title: "Attempt 2", status: "Accepted", date: "2024-06-02" },
	{ title: "Attempt 3", status: "Rejected", date: "2024-06-03" },
	{ title: "Attempt 4", status: "Accepted", date: "2024-06-04" },
	{ title: "Attempt 5", status: "Pending", date: "2024-06-05" },
];

usePageMeta(() => ({
	title: pageTitle("Attempts"),
}));
</script>

<template>
	<div class="container mx-auto max-w-3xl py-16">
		<div class="divide-y">
			<div class="flex pb-4 font-medium">
				<div class="w-1/2">Title</div>
				<div class="w-1/4 text-end">Date</div>
				<div class="w-1/4 text-end">Status</div>
			</div>
			<div v-for="attempt in attempts" :key="attempt.title" class="flex py-4 cursor-pointer">
				<div class="w-1/2">{{ attempt.title }}</div>
				<div class="w-1/4 text-end">{{ attempt.date }}</div>
				<div class="w-1/4 text-end">
					<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
				</div>
			</div>
		</div>
	</div>
</template>
