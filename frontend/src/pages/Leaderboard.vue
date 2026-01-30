<script setup lang="ts">
import { Avatar, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";

const leaderboard = [
	{ name: "Alice", score: 150 },
	{ name: "Bob", score: 120 },
	{ name: "Charlie", score: 100 },
	{ name: "Diana", score: 90 },
	{ name: "Eve", score: 80 },
	{ name: "Frank", score: 70 },
	{ name: "Grace", score: 60 },
	{ name: "Heidi", score: 50 },
	{ name: "Ivan", score: 40 },
	{ name: "Judy", score: 30 },
	{ name: "Mallory", score: 20 },
	{ name: "Niaj", score: 10 },
	{ name: "Olivia", score: 5 },
	{ name: "Peggy", score: 2 },
	{ name: "Sybil", score: 1 },
];

usePageMeta(() => ({
	title: pageTitle("Leaderboard"),
}));
</script>

<template>
	<div class="container mx-auto py-8">
		<div class="divide-y">
			<div class="flex justify-between items-center font-medium pb-4">
				<p class="ml-9">Hunter</p>
				<p>Score</p>
			</div>
			<div v-for="hunter in leaderboard" class="py-4 flex justify-between items-center">
				<div class="flex items-center gap-2">
					<Avatar :label="hunter.name" size="lg" />
					<p>{{ hunter.name }}</p>
				</div>
				<p>{{ hunter.score }}</p>
			</div>
		</div>
	</div>
</template>
