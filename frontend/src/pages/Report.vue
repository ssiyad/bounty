<script setup lang="ts">
import ReportDetails from "@/components/report/ReportDetails.vue";
import Chat from "@/components/report/Chat.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { createDocumentResource } from "frappe-ui";
import { computed, ref, watchEffect } from "vue";
import { useRoute } from "vue-router";
import DOMPurify from "dompurify";
import ChevronDownIcon from "~icons/lucide/chevron-down";
import ChevronUpIcon from "~icons/lucide/chevron-up";

const route = useRoute();
const id = route.params.id as string;

const report = createDocumentResource({
	doctype: "FS Report",
	name: id,
	cache: ["report", id],
	auto: true,
});

const { set } = useBreadcrumbs();

const showDetails = ref(false);

const sanitizedContent = computed(() => {
	if (!report.doc?.content) return "";
	return DOMPurify.sanitize(report.doc.content);
});

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
	<div v-if="report.doc" class="flex flex-col md:flex-row min-h-0 grow">
		<div class="grow overflow-y-auto">
			<div class="py-6 md:py-14 max-w-[840px] mx-auto px-4 md:px-0">
				<div class="text-2xl md:text-3xl font-semibold mb-4 pb-6 border-b">
					{{ report.doc.title }}
				</div>
				<div
					v-html="sanitizedContent"
					class="prose prose-sm max-w-none leading-relaxed mb-8"
				/>
				<Chat :report="id" />
			</div>
		</div>
		<!-- Mobile collapsible details -->
		<div class="md:hidden border-t">
			<button
				class="w-full flex items-center justify-between px-4 py-3 text-sm font-medium"
				@click="showDetails = !showDetails"
			>
				<span>Details</span>
				<component :is="showDetails ? ChevronUpIcon : ChevronDownIcon" class="w-4 h-4" />
			</button>
			<div v-show="showDetails" class="px-4 pb-4">
				<ReportDetails :id="id" :doc="report.doc" />
			</div>
		</div>
		<!-- Desktop sidebar -->
		<div class="hidden md:block md:w-72 shrink-0 px-5 py-4 border-l">
			<ReportDetails :id="id" :doc="report.doc" />
		</div>
	</div>
</template>
