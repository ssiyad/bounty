<script setup lang="ts">
import { Button, Textarea, TextInput } from "frappe-ui";
import { ref } from "vue";

const title = ref("");
const content = ref("");

const cancel = () => (content.value = "");
const submit = () => {};
</script>

<template>
	<div class="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
		<div class="max-w-3xl mx-auto min-w-[700px]">
			<div class="mb-8 space-y-2 text-2xl text-gray-800">
				<p>
					Found a <span class="text-gray-900 font-medium">security</span> issue with a
					<span class="text-gray-900 font-medium">Frappe</span> product?
				</p>
				<p>
					<span class="text-gray-900 font-medium">Report</span> it and get
					<span class="text-gray-900 font-medium">rewarded</span>!
				</p>
			</div>
			<TextInput v-model="title" type="text" placeholder="Title" class="mb-2" />
			<Textarea
				v-model="content"
				variant="subtle"
				placeholder="Explain the problem..."
				class="mb-2 min-h-40"
			/>
			<div class="space-x-2 text-end">
				<Button label="Cancel" @click="cancel" />
				<Button label="Submit" variant="solid" @click="submit" />
			</div>
		</div>
	</div>
</template>
