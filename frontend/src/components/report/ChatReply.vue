<script setup lang="ts">
import { onUnmounted, ref } from "vue";
import { Dialog, Textarea, Button } from "frappe-ui";

defineProps<{
	modelValue: boolean;
}>();

const emit = defineEmits<{
	(e: "update:modelValue", value: boolean): void;
	(e: "send", content: string): void;
}>();

const content = ref("");

onUnmounted(() => {
	content.value = "";
});

const send = () => {
	emit("send", content.value);
	emit("update:modelValue", false);
};
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
