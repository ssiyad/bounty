<script setup lang="ts">
import Attachments from "@/components/Attachments.vue";
import Target from "@/components/Target.vue";
import SeverityBadge from "@/components/badges/SeverityBadge.vue";
import StatusBadge from "@/components/badges/StatusBadge.vue";
import { categoryTheme } from "@/utils/badgeThemes";
import { Badge } from "frappe-ui";

interface ReportDoc {
	target: string;
	status: string;
	category: string;
	severity: string;
}

defineProps<{
	id: string;
	doc: ReportDoc;
}>();
</script>

<template>
	<div class="space-y-3">
		<div v-if="doc.target" class="flex items-center justify-between">
			<p class="text-sm">Target</p>
			<Target :target="doc.target" />
		</div>
		<hr v-if="doc.target" />
		<div class="flex items-center justify-between">
			<p class="text-sm">Status</p>
			<StatusBadge :status="doc.status" />
		</div>
		<div class="flex items-center justify-between">
			<p class="text-sm">Category</p>
			<div>
				<Badge :label="doc.category" :theme="categoryTheme(doc.category)" />
			</div>
		</div>
		<div class="flex items-center justify-between">
			<p class="text-sm">Severity</p>
			<SeverityBadge :severity="doc.severity" />
		</div>
		<Attachments class="pt-3 border-t" readonly doctype="FS Report" :docname="id" />
	</div>
</template>