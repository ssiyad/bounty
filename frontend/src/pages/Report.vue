<script setup lang="ts">
import { watchEffect } from "vue";
import { useRoute } from "vue-router";
import { Badge, createResource } from "frappe-ui";
import { statusTheme, categoryTheme, severityTheme } from "@/utils/badgeThemes";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Chat from "@/components/report/Chat.vue";
import Target from "@/components/Target.vue";

const route = useRoute();
const id = route.params.id as string;

const report = createResource({
	url: "bounty.api.report.get_report",
	auto: !!id,
	cache: ["report", id],
	makeParams: () => ({
		name: id,
	}),
});

const { set } = useBreadcrumbs();

watchEffect(() => {
	set([
		{
			label: "Reports",
			route: { name: "Reports" },
		},
		{
			label: report.data?.title ?? id,
		},
	]);
});
</script>

<template>
	<div v-if="report.data" class="flex divide-x size-full">
		<div class="grow px-5 py-8 overflow-y-auto">
			<div class="text-3xl font-semibold mb-4">
				{{ report.data.title }}
			</div>
			<p class="leading-relaxed mb-8">
				{{ report.data.content }}
			</p>
			<Chat :report="id" />
		</div>
		<div class="w-72 shrink-0 px-4 py-4 space-y-4">
			<div v-if="report.data.target" class="flex items-center justify-between">
				<p class="text-sm">Target</p>
				<Target :target="report.data.target" />
			</div>
			<hr v-if="report.data.target" />
			<div class="flex items-center justify-between">
				<p class="text-sm">Status</p>
				<div>
					<Badge :label="report.data.status" :theme="statusTheme(report.data.status)" />
				</div>
			</div>
			<div class="flex items-center justify-between">
				<p class="text-sm">Category</p>
				<div>
					<Badge
						:label="report.data.category"
						:theme="categoryTheme(report.data.category)"
					/>
				</div>
			</div>
			<div class="flex items-center justify-between">
				<p class="text-sm">Severity</p>
				<div>
					<Badge
						:label="report.data.severity"
						:theme="severityTheme(report.data.severity)"
					/>
				</div>
			</div>
		</div>
	</div>
</template>
