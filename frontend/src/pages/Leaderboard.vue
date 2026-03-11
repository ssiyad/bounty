<script setup lang="ts">
import { Avatar, createResource } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";

useBreadcrumbs().set([{ label: "Leaderboard" }]);

const leaderboard = createResource({
	url: "bounty.api.leaderboard.get_leaderboard",
	auto: true,
});
</script>

<template>
	<div v-if="leaderboard.data" class="overflow-auto">
		<div class="divide-y">
			<div class="h-12.5 px-5 py-4 flex justify-between items-center font-medium">
				<p class="ml-9">Hunter</p>
				<p>Score</p>
			</div>
			<div
				v-for="hunter in leaderboard.data"
				:key="hunter.name"
				class="h-12.5 px-5 py-4 flex justify-between items-center"
			>
				<div class="flex items-center gap-2">
					<Avatar :label="hunter.name" size="lg" />
					<p>{{ hunter.name }}</p>
				</div>
				<p>{{ hunter.score }}</p>
			</div>
		</div>
	</div>
</template>
