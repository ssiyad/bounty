<script setup lang="ts">
import {
	Button,
	TextEditor,
	TextEditorFixedMenu,
	createResource,
} from "frappe-ui";
import { ref } from "vue";

const props = withDefaults(
	defineProps<{
		report?: string;
	}>(),
	{
		report: "",
	},
);

const buttons = [
	"Paragraph",
	["Heading 2", "Heading 3", "Heading 4"],
	"Separator",
	"Bold",
	"Italic",
	"Separator",
	"Bullet List",
	"Numbered List",
	"Separator",
	"Link",
	"Image",
];

const messages = createResource({
	url: "security.api.chat.get_messages",
	auto: !!props.report,
	makeParams: () => ({
		report: props.report,
	}),
	initialData: [],
});

const message = ref("");

const cancel = () => (message.value = "");

const send = () => {
	createResource({
		url: "security.api.chat.send_message",
		method: "POST",
		auto: true,
		params: {
			report: props.report,
			content: message.value,
		},
		onSuccess: (messages_: any) => {
			message.value = "";
			messages.setData(messages_);
		},
	});
};
</script>

<template>
	<div>
		<hr />
		<div class="space-y-4 py-4">
			<TextEditor
				class="border px-3 py-2 rounded-md"
				editor-class="prose-sm leading-relaxed max-w-none overflow-y-auto min-h-14 max-h-60 resize-y"
				placeholder="What do you want to tell the team?"
				:content="message"
				@change="message = $event"
			>
				<template #bottom>
					<div class="mt-2 flex flex-col justify-between sm:flex-row sm:items-center">
						<TextEditorFixedMenu class="-ml-1 overflow-x-auto" :buttons="buttons" />
						<div class="mt-2 flex items-center justify-end space-x-2 sm:mt-0">
							<Button variant="ghost" @click="cancel">Cancel</Button>
							<Button variant="subtle" @click="send">Send</Button>
						</div>
					</div>
				</template>
			</TextEditor>
			<div v-if="messages.data.length" class="w-max flex gap-4 text-sm text-center">
				<div class="flex items-center gap-2">
					<div class="bg-surface-gray-2 size-4 border rounded-full"></div>
					<p>Frappe</p>
				</div>
				<div class="flex items-center gap-2">
					<div class="bg-surface-blue-1 size-4 border rounded-full"></div>
					<p>You</p>
				</div>
			</div>
			<div v-for="message in messages.data" :key="message.id">
				<div
					v-html="message.content"
					:class="{
						'bg-surface-gray-2': message.sent_or_received === 'Received',
						'bg-surface-blue-1 ml-auto mr-0': message.sent_or_received === 'Sent',
					}"
					class="max-w-2xl w-max prose prose-sm leading-relaxed px-4 py-2 rounded-lg text-ink-gray-8"
				/>
			</div>
		</div>
	</div>
</template>
