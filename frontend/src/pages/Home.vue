<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Button, Textarea, TextInput, createResource, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";

const router = useRouter();
const title = ref("");
const content = ref("");

const cancel = () => (content.value = "");
const submit = () => {
	createResource({
		url: "frappe.client.insert",
		method: "POST",
		auto: true,
		makeParams: () => ({
			doc: {
				doctype: "Bounty Attempt",
				title: title.value,
				content: content.value,
			},
		}),
		onSuccess: (attempt: any) => {
			router.push({
				name: "Attempt",
				params: {
					id: attempt.name,
				},
			});
		},
	});
};

usePageMeta(() => ({
	title: pageTitle("Report an Issue"),
}));
</script>

<template>
	<div class="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
		<div class="max-w-3xl mx-auto min-w-[700px]">
			<div class="mb-8 space-y-2 text-2xl text-ink-gray-8 font-medium">
				<p>
					Found a <span class="text-ink-gray-9 font-semibold">security</span> issue with
					a <span class="text-ink-gray-9 font-semibold">Frappe</span> product?
				</p>
				<p>
					<span class="text-ink-gray-9 font-semibold">Report</span> it and earn
					<span class="text-ink-gray-9 font-semibold">rewards</span>!
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
				<Button label="Submit" variant="solid" icon-right="arrow-right" @click="submit" />
			</div>
		</div>
	</div>
</template>
