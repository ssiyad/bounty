<script setup lang="ts">
import { onUnmounted, ref } from "vue";
import { Dialog, Textarea, Button, createResource } from "frappe-ui";

const props = withDefaults(
	defineProps<{
		modelValue: boolean;
		report?: string;
	}>(),
	{
		report: "",
	},
);

const emit = defineEmits<{
	(e: "update:modelValue", value: boolean): void;
	(e: "sent", messages: any): void;
}>();

const content = ref("");

const send = () => {
	createResource({
		url: "bounty.api.chat.send_message",
		method: "POST",
		auto: true,
		params: {
			report: props.report,
			content: content.value,
		},
		onSuccess: (messages: any) => {
			emit("sent", messages);
			emit("update:modelValue", false);
			content.value = "";
		},
	});
};

onUnmounted(() => {
	content.value = "";
});
</script>

<template>
	<Dialog
		:model-value="modelValue"
		@update:model-value="$emit('update:modelValue', $event)"
		size="md"
		:options="{
			title: 'Reply',
			size: 'xl',
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<p class="text-ink-gray-8">What would you like to tell the team?</p>
				<Textarea v-model="content" placeholder="Jot down your thoughts..." class="h-32" />
			</div>
		</template>
		<template #actions="{ close }">
			<div class="flex flex-row-reverse gap-2">
				<Button variant="solid" @click="send">Send</Button>
				<Button variant="outline" @click="close">Cancel</Button>
			</div>
		</template>
	</Dialog>
</template>
