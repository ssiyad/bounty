<script setup lang="ts">
import ReportListItem from "@/components/list/ReportListItem.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { Button, createListResource } from "frappe-ui";

useBreadcrumbs().set([{ label: "Reports" }]);

const reports = createListResource({
	doctype: "FS Report",
	cache: ["reports"],
	auto: true,
	fields: ["name", "title", "target", "creation", "status"],
	orderBy: "modified desc",
});
</script>

<template>
	<Teleport defer to="#topbar-actions">
		<RouterLink
			:to="{
				name: 'Draft',
				params: {
					id: 'draft',
				},
			}"
		>
			<Button label="Report" icon-left="plus" variant="solid" />
		</RouterLink>
	</Teleport>
	<div class="divide-y grow min-h-0 overflow-y-auto">
		<!-- Desktop table header -->
		<div class="hidden md:flex h-12 px-5 py-4 font-medium bg-surface-gray-1">
			<div class="grow">Title</div>
			<div class="w-[180px] text-end">Target</div>
			<div class="w-[200px] text-end">Date</div>
			<div class="w-[150px] text-end">Status</div>
		</div>
		<ReportListItem
			v-for="report in reports.data"
			:key="report.name"
			:report="report"
		/>
	</div>
	<div class="h-12 shrink-0 flex items-center justify-end px-4 md:px-5 border-t">
		<Button
			label="Load More"
			:loading="reports.loading"
			:disabled="!reports.hasNextPage"
			@click="reports.next()"
		/>
	</div>
</template>