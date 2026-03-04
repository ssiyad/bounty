<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Badge, createDocumentResource } from "frappe-ui";
import Chat from "../components/report/Chat.vue";
import Target from "../components/Target.vue";
import { statusTheme, categoryTheme, severityTheme } from "../utils/badgeThemes";
import PageLayout from "../layouts/PageLayout.vue";

const route = useRoute();
const id = route.params.id as string;

const reportResource = createDocumentResource({
	doctype: "Bounty Report",
	name: id,
	cache: ["Report", id],
	auto: !!id,
	whitelistedMethods: {
		chat: {
			method: "chat",
			auto: true,
			initialData: [],
		},
		reply: {
			method: "reply",
			onSuccess: (messages: any[]) => {
				reportResource.chat.setData(messages);
			},
		},
	},
});

const report = computed(() => reportResource.doc);

const breadcrumbs = computed(() => [
	{
		label: "Reports",
		route: {
			name: "Reports",
		},
	},
	{
		label: reportResource.doc?.title,
	},
]);
</script>

<template>
	<PageLayout class="size-full" :breadcrumbs="breadcrumbs">
		<div v-if="report" class="flex divide-x size-full">
			<div class="px-5 py-8 overflow-y-auto">
				<div class="text-3xl font-semibold mb-4">
					{{ report.title }}
				</div>
				<p class="leading-relaxed mb-8">
					{{ report.content }}
				</p>
				<Chat
					:messages="reportResource.chat.data"
					@reply="
						reportResource.reply.submit({
							content: $event,
						})
					"
				/>
			</div>
			<div class="w-72 shrink-0 px-4 py-4 space-y-4">
				<div v-if="report.target" class="flex items-center justify-between">
					<p class="text-sm">Target</p>
					<Target :target="report.target" />
				</div>
				<hr v-if="report.target" />
				<div class="flex items-center justify-between">
					<p class="text-sm">Status</p>
					<div>
						<Badge :label="report.status" :theme="statusTheme(report.status)" />
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Category</p>
					<div>
						<Badge :label="report.category" :theme="categoryTheme(report.category)" />
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Severity</p>
					<div>
						<Badge :label="report.severity" :theme="severityTheme(report.severity)" />
					</div>
				</div>
			</div>
		</div>
	</PageLayout>
</template>
