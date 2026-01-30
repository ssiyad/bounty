<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Avatar, Badge, Button, createDocumentResource, usePageMeta } from "frappe-ui";
import { statusTheme, categoryTheme, severityTheme } from "../utils/badgeThemes";
import { pageTitle } from "../utils/page";

const route = useRoute();
const attemptId = route.params.id as string;

const attemptResource = createDocumentResource({
	doctype: "Bounty Attempt",
	name: attemptId,
	auto: !!attemptId,
});

const attempt = computed(() => attemptResource.doc);

const targetResource = createDocumentResource({
	doctype: "Bounty Target",
	name: attempt.value?.target,
	cache: ["Bounty Target", attempt.value?.target],
	auto: !!attempt.value?.target,
});

const target = computed(() => targetResource.doc);

const chat = [
	{
		content: "Hello, how can I help you?",
		sent_or_received: "Received",
		date: "2024-01-01",
	},
	{
		content: "I have a question about my order.",
		sent_or_received: "Sent",
		date: "2024-01-01",
	},
	{
		content:
			"This is a very long text message to demonstrate how the chat bubbles will handle larger amounts of text. It should wrap properly and still look good in the UI.",
		sent_or_received: "Sent",
		date: "2024-01-01",
	},
	{
		content: "Sure, can you provide your order number?",
		sent_or_received: "Received",
		date: "2024-01-01",
	},
	{
		content: "Yes, it's 12345.",
		sent_or_received: "Sent",
		date: "2024-01-01",
	},
].reverse();

usePageMeta(() => ({
	title: pageTitle(attempt.value?.title),
}));
</script>

<template>
	<div class="container mx-auto py-16">
		<div v-if="attempt" class="flex divide-x">
			<div class="pr-4">
				<div class="text-3xl font-medium mb-4">
					{{ attempt.title }}
				</div>
				<p class="leading-relaxed mb-8">
					{{ attempt.content }}
				</p>
				<hr />
				<div class="space-y-4 py-4">
					<div class="w-max ml-auto mr-0 flex gap-4 text-sm text-center">
						<div class="flex items-center gap-2">
							<div class="bg-surface-gray-2 size-4 border rounded-full"></div>
							<p>Frappe</p>
						</div>
						<div class="flex items-center gap-2">
							<div class="bg-surface-blue-1 size-4 border rounded-full"></div>
							<p>You</p>
						</div>
						<Button label="Reply" variant="outline" />
					</div>
					<div v-for="message in chat" :key="message.content">
						<div
							:class="{
								'bg-surface-gray-2': message.sent_or_received === 'Received',
								'bg-surface-blue-1 ml-auto mr-0':
									message.sent_or_received === 'Sent',
							}"
							class="max-w-lg w-max leading-relaxed px-4 py-2 rounded-lg text-ink-gray-8"
						>
							{{ message.content }}
						</div>
					</div>
				</div>
			</div>
			<div class="w-64 shrink-0 pl-4 py-4 space-y-4">
				<div v-if="target" class="flex items-center justify-between">
					<p class="text-sm">Target</p>
					<a :href="target.repository" target="_blank">
						<div class="flex items-center gap-2">
							<img
								v-if="target.logo"
								class="flex size-6 items-center justify-center rounded-[5px]"
								:src="target.logo"
								:alt="target.name"
							/>
							<Avatar v-else :label="target.name" shape="square" />
							<div class="font-medium">
								{{ attempt.target }}
							</div>
						</div>
					</a>
				</div>
				<hr v-if="target" />
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
