<script setup lang="ts">
import Target from "@/components/Target.vue";
import { formatDate } from "date-fns";
import { Badge, Button, createListResource } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { statusTheme } from "@/utils/badgeThemes";

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
					id: 'new-report',
				},
			}"
		>
			<Button label="Report" icon-left="plus" variant="solid" />
		</RouterLink>
	</Teleport>
	<div class="divide-y grow min-h-0 overflow-y-auto">
		<div class="flex h-12 px-5 py-4 font-medium bg-surface-gray-1">
			<div class="grow">Title</div>
			<div class="w-[180px] text-end">Target</div>
			<div class="w-[200px] text-end">Date</div>
			<div class="w-[150px] text-end">Status</div>
		</div>
		<RouterLink
			v-for="report in reports.data"
			:key="report.name"
			:to="{
				name: 'Report',
				params: {
					id: report.name,
				},
			}"
			class="block"
		>
			<div class="flex h-12 px-5 py-4 cursor-pointer">
				<div class="grow">{{ report.title }}</div>
				<div class="w-[180px] text-end">
					<Target v-if="report.target" :target="report.target" class="ml-auto mr-0" />
					<span v-else>&mdash;</span>
				</div>
				<div class="w-[200px] text-end">
					{{ formatDate(report.creation, "PPP") }}
				</div>
				<div class="w-[150px] text-end">
					<Badge :label="report.status" :theme="statusTheme(report.status)" />
				</div>
			</div>
		</RouterLink>
	</div>
	<div class="h-12 shrink-0 flex items-center justify-end px-5 border-t">
		<Button
			label="Load More"
			:loading="reports.loading"
			:disabled="!reports.hasNextPage"
			@click="reports.next()"
		/>
	</div>
</template>
