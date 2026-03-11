<script setup lang="ts">
import { ref } from "vue";
import { Button, createResource } from "frappe-ui";
import ChatReply from "./ChatReply.vue";

const props = withDefaults(
	defineProps<{
		report?: string;
	}>(),
	{
		report: "",
	},
);

const isReplyOpen = ref(false);

const messages = createResource({
	url: "bounty.api.chat.get_messages",
	auto: !!props.report,
	makeParams: () => ({
		report: props.report,
	}),
});
</script>

<template>
	<div>
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
				<Button label="Reply" variant="outline" @click="isReplyOpen = true" />
			</div>
			<div v-for="message in messages.data" :key="message.id">
				<div
					:class="{
						'bg-surface-gray-2': message.sent_or_received === 'Received',
						'bg-surface-blue-1 ml-auto mr-0': message.sent_or_received === 'Sent',
					}"
					class="max-w-2xl w-max leading-relaxed px-4 py-2 rounded-lg text-ink-gray-8"
				>
					{{ message.content }}
				</div>
			</div>
		</div>
		<ChatReply
			v-model="isReplyOpen"
			:report="props.report"
			@sent="
				(messages_: typeof messages.data) => {
					isReplyOpen = false;
					messages.setData(messages_);
				}
			"
		/>
	</div>
</template>
