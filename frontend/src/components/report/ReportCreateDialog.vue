<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Button, Dialog, Textarea, TextInput, createResource } from "frappe-ui";
const router = useRouter();
const title = ref("");
const content = ref("");

withDefaults(
	defineProps<{
		modelValue?: boolean;
	}>(),
	{
		modelValue: false,
	},
);

defineEmits<{
	"update:modelValue": [boolean];
}>();

const submit = () => {
	createResource({
		url: "bounty.api.report.create_report",
		method: "POST",
		auto: true,
		params: {
			title: title.value,
			content: content.value,
		},
		onSuccess: (name: string) => {
			router.push({
				name: "Report",
				params: {
					id: name,
				},
			});
		},
	});
};

const onClose = () => {
	title.value = "";
	content.value = "";
};
</script>

<template>
	<Dialog
		:model-value="modelValue"
		:options="{
			size: '3xl',
			title: 'Report an Issue',
		}"
		@update:model-value="$emit('update:modelValue', $event)"
		@close="onClose"
	>
		<template #body-content>
			<div class="">
				<TextInput v-model="title" type="text" placeholder="Title" class="mb-2" />
				<Textarea
					v-model="content"
					variant="subtle"
					placeholder="Explain the problem..."
					class="mb-4 min-h-40"
				/>
				<div class="space-x-2 text-end">
					<Button
						label="Submit"
						variant="solid"
						icon-right="arrow-right"
						@click="submit"
					/>
				</div>
			</div>
		</template>
	</Dialog>
</template>
