<script setup lang="ts">
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { Avatar, createResource } from "frappe-ui";

useBreadcrumbs().set([{ label: "Leaderboard" }]);

const leaderboard = createResource({
	url: "security.api.leaderboard.get_leaderboard",
	auto: true,
});
</script>

<template>
	<div v-if="leaderboard.data" class="overflow-auto">
		<div class="divide-y">
			<div class="hidden md:flex h-12.5 px-5 py-4 justify-between items-center font-medium">
				<p class="ml-9">Hunter</p>
				<p>Score</p>
			</div>
			<div
				v-for="hunter in leaderboard.data"
				:key="hunter.name"
				class="h-12.5 px-4 md:px-5 py-4 flex justify-between items-center"
			>
				<div class="flex items-center gap-2">
					<Avatar :label="hunter.name" size="lg" />
					<p>{{ hunter.name }}</p>
				</div>
				<p class="text-ink-gray-7">{{ hunter.score }}</p>
			</div>
		</div>
	</div>
</template>
