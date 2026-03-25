<script setup lang="ts">
import { watchEffect } from "vue";
import { useRoute } from "vue-router";
import { Badge, createResource } from "frappe-ui";
import { categoryTheme } from "@/utils/badgeThemes";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Chat from "@/components/report/Chat.vue";
import Target from "@/components/Target.vue";
import SeverityBadge from "@/components/badges/SeverityBadge.vue";
import StatusBadge from "@/components/badges/StatusBadge.vue";

const route = useRoute();
const id = route.params.id as string;

const report = createResource({
	url: "security.api.report.get_report",
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
	<div v-if="report.data" class="flex divide-x min-h-0">
		<div class="grow overflow-y-auto">
			<div class="py-14 max-w-[840px] mx-auto">
				<div class="text-3xl font-semibold mb-4 pb-6 border-b">
					{{ report.data.title }}
				</div>
				<div
					v-html="report.data.content"
					class="prose prose-sm max-w-none leading-relaxed mb-8"
				/>
				<Chat :report="id" />
			</div>
		</div>
		<div class="w-72 shrink-0 px-4 py-4 space-y-4">
			<div v-if="report.data.target" class="flex items-center justify-between">
				<p class="text-sm">Target</p>
				<Target :target="report.data.target" />
			</div>
			<hr v-if="report.data.target" />
			<div class="flex items-center justify-between">
				<p class="text-sm">Status</p>
				<StatusBadge :status="report.data.status" />
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
				<SeverityBadge :severity="report.data.severity" />
			</div>
		</div>
	</div>
</template>
