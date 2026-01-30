<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Badge, createDocumentResource, usePageMeta } from "frappe-ui";
import Chat from "../components/attempt/Chat.vue";
import Target from "../components/Target.vue";
import { statusTheme, categoryTheme, severityTheme } from "../utils/badgeThemes";
import { pageTitle } from "../utils/page";

const route = useRoute();
const attemptId = route.params.id as string;

const attemptResource = createDocumentResource({
	doctype: "Bounty Attempt",
	name: attemptId,
	auto: !!attemptId,
	whitelistedMethods: {
		chat: {
			method: "chat",
			auto: true,
			initialData: [],
		},
		reply: {
			method: "reply",
			onSuccess: (messages: any[]) => {
				attemptResource.chat.setData(messages);
			},
		},
	},
});

const attempt = computed(() => attemptResource.doc);

usePageMeta(() => ({
	title: pageTitle(attempt.value?.title),
}));
</script>

<template>
	<div class="size-full">
		<div v-if="attempt" class="flex divide-x size-full">
			<div class="container mx-auto py-8 overflow-y-auto">
				<div class="text-3xl font-medium mb-4">
					{{ attempt.title }}
				</div>
				<p class="leading-relaxed mb-8">
					{{ attempt.content }}
				</p>
				<Chat
					:messages="attemptResource.chat.data"
					@reply="
						attemptResource.reply.submit({
							content: $event,
						})
					"
				/>
			</div>
			<div class="w-72 shrink-0 px-4 py-4 space-y-4">
				<div v-if="attempt.target" class="flex items-center justify-between">
					<p class="text-sm">Target</p>
					<Target :target="attempt.target" />
				</div>
				<hr v-if="attempt.target" />
				<div class="flex items-center justify-between">
					<p class="text-sm">Status</p>
					<div>
						<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Category</p>
					<div>
						<Badge
							:label="attempt.category"
							:theme="categoryTheme(attempt.category)"
						/>
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Severity</p>
					<div>
						<Badge
							:label="attempt.severity"
							:theme="severityTheme(attempt.severity)"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
