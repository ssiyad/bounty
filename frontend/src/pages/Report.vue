<script setup lang="ts">
import { watchEffect } from "vue";
import { useRoute } from "vue-router";
import { Badge, createDocumentResource } from "frappe-ui";
import { categoryTheme } from "@/utils/badgeThemes";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Attachments from "@/components/Attachments.vue";
import Chat from "@/components/report/Chat.vue";
import Target from "@/components/Target.vue";
import SeverityBadge from "@/components/badges/SeverityBadge.vue";
import StatusBadge from "@/components/badges/StatusBadge.vue";

const route = useRoute();
const id = route.params.id as string;

const report = createDocumentResource({
	doctype: "FS Report",
	name: id,
	cache: ["report", id],
	auto: true,
});

const { set } = useBreadcrumbs();

watchEffect(() => {
	set([
		{
			label: "Reports",
			route: { name: "Reports" },
		},
		{
			label: report.doc?.title ?? id,
		},
	]);
});
</script>

<template>
	<div v-if="report.doc" class="flex divide-x min-h-0 grow">
		<div class="grow overflow-y-auto">
			<div class="py-14 max-w-[840px] mx-auto">
				<div class="text-3xl font-semibold mb-4 pb-6 border-b">
					{{ report.doc.title }}
				</div>
				<div
					v-html="report.doc.content"
					class="prose prose-sm max-w-none leading-relaxed mb-8"
				/>
				<Chat :report="id" />
			</div>
		</div>
		<div class="w-72 shrink-0 px-5 py-4 space-y-3">
			<div v-if="report.doc.target" class="flex items-center justify-between">
				<p class="text-sm">Target</p>
				<Target :target="report.doc.target" />
			</div>
			<hr v-if="report.doc.target" />
			<div class="flex items-center justify-between">
				<p class="text-sm">Status</p>
				<StatusBadge :status="report.doc.status" />
			</div>
			<div class="flex items-center justify-between">
				<p class="text-sm">Category</p>
				<div>
					<Badge
						:label="report.doc.category"
						:theme="categoryTheme(report.doc.category)"
					/>
				</div>
			</div>
			<div class="flex items-center justify-between">
				<p class="text-sm">Severity</p>
				<SeverityBadge :severity="report.doc.severity" />
			</div>
			<Attachments class="pt-3 border-t" readonly doctype="FS Report" :docname="id" />
		</div>
	</div>
</template>
