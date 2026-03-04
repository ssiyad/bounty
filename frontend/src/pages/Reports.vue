<script setup lang="ts">
import { ref } from "vue";
import { formatDate } from "date-fns";
import { Badge, Button, createListResource } from "frappe-ui";
import Target from "../components/Target.vue";
import { statusTheme } from "../utils/badgeThemes";
import PageLayout from "../layouts/PageLayout.vue";
import ReportCreateDialog from "../components/report/ReportCreateDialog.vue";

const reports = createListResource({
	doctype: "Bounty Report",
	cache: ["Reports"],
	fields: ["name", "title", "creation", "status", "target"],
	orderBy: "creation desc",
	pageLength: 99999,
	auto: true,
});

const breadcrumbs = [
	{
		label: "Reports",
	},
];

const isReportDialogOpen = ref(false);
</script>

<template>
	<ReportCreateDialog v-model="isReportDialogOpen" />
	<PageLayout :breadcrumbs="breadcrumbs">
		<template #actions>
			<Button
				label="Report"
				icon-left="plus"
				variant="solid"
				@click="isReportDialogOpen = true"
			/>
		</template>
		<div class="divide-y">
			<div class="flex h-12 px-5 py-4 font-medium">
				<div class="grow">Title</div>
				<div class="w-[180px] text-end">Target</div>
				<div class="w-[200px] text-end">Date</div>
				<div class="w-[150px] text-end">Status</div>
			</div>
			<RouterLink
				v-for="reports in reports.data"
				:to="{
					name: 'Report',
					params: { id: reports.name },
				}"
				class="block"
			>
				<div :key="reports.name" class="flex h-12 px-5 py-4 cursor-pointer">
					<div class="grow">{{ reports.title }}</div>
					<div class="w-[180px] text-end">
						<Target
							v-if="reports.target"
							:target="reports.target"
							class="ml-auto mr-0"
						/>
						<span v-else>&mdash;</span>
					</div>
					<div class="w-[200px] text-end">{{ formatDate(reports.creation, "PPP") }}</div>
					<div class="w-[150px] text-end">
						<Badge :label="reports.status" :theme="statusTheme(reports.status)" />
					</div>
				</div>
			</RouterLink>
		</div>
	</PageLayout>
</template>
