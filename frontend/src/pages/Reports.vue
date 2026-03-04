<script setup lang="ts">
import { formatDate } from "date-fns";
import { Badge, Button, createListResource } from "frappe-ui";
import Target from "../components/Target.vue";
import { statusTheme } from "../utils/badgeThemes";
import PageLayout from "../layouts/PageLayout.vue";

const attemptsResource = createListResource({
	doctype: "Bounty Attempt",
	cache: ["Reports"],
	fields: ["name", "title", "creation", "status", "target"],
	orderBy: "creation desc",
	pageLength: 99999,
	auto: true,
});
</script>

<template>
	<PageLayout>
		<template #actions>
			<Button label="Report" icon-left="plus" variant="solid" />
		</template>
		<div class="divide-y">
			<div class="flex h-12 px-5 py-4 font-medium">
				<div class="grow">Title</div>
				<div class="w-[180px] text-end">Target</div>
				<div class="w-[200px] text-end">Date</div>
				<div class="w-[150px] text-end">Status</div>
			</div>
			<RouterLink
				v-for="attempt in attemptsResource.data"
				:to="{
					name: 'Report',
					params: { id: attempt.name },
				}"
				class="block"
			>
				<div :key="attempt.name" class="flex h-12 px-5 py-4 cursor-pointer">
					<div class="grow">{{ attempt.title }}</div>
					<div class="w-[180px] text-end">
						<Target
							v-if="attempt.target"
							:target="attempt.target"
							class="ml-auto mr-0"
						/>
						<span v-else>&mdash;</span>
					</div>
					<div class="w-[200px] text-end">{{ formatDate(attempt.creation, "PPP") }}</div>
					<div class="w-[150px] text-end">
						<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
					</div>
				</div>
			</RouterLink>
		</div>
	</PageLayout>
</template>
