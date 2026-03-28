<script setup lang="ts">
import { Button, FileUploader, createListResource, createResource } from "frappe-ui";
import Attachment from "./Attachment.vue";
import UploadIcon from "~icons/lucide/upload";

const props = withDefaults(
	defineProps<{
		doctype: string;
		docname: string;
		readonly?: boolean;
	}>(),
	{
		readonly: false,
	},
);

const attachments = createListResource({
	doctype: "File",
	auto: true,
	filters: {
		attached_to_doctype: props.doctype,
		attached_to_name: props.docname,
	},
	fields: ["name", "file_name", "file_url"],
});

const remove = (docname: string) => {
	createResource({
		url: "frappe.client.delete",
		auto: true,
		method: "POST",
		params: {
			doctype: "File",
			name: docname,
		},
		onSuccess: () => {
			attachments.data = attachments.data?.filter((a: any) => a.name !== docname) ?? [];
		},
	});
};
</script>

<template>
	<div
		:class="{
			hidden: readonly && !attachments.data?.length,
		}"
	>
		<div class="h-7 mb-2 flex items-center justify-between">
			<div class="text-sm font-medium">Attachments</div>
			<FileUploader
				v-if="!readonly"
				:upload-args="{
					doctype: doctype,
					docname: docname,
					private: true,
					optimize: true,
				}"
				@success="attachments.data.push($event)"
			>
				<template #default="{ uploading, openFileSelector }">
					<Button
						label="Upload"
						:icon="UploadIcon"
						:loading="uploading"
						@click="openFileSelector"
					/>
				</template>
			</FileUploader>
		</div>
		<div
			v-for="attachment in attachments.data"
			class="group h-7 flex items-center justify-between"
		>
			<Attachment :name="attachment.file_name" :url="attachment.file_url" />
			<Button
				v-if="!readonly"
				class="opacity-0 group-hover:opacity-100"
				label="Upload"
				variant="ghost"
				icon="x"
				@click="remove(attachment.name)"
			/>
		</div>
	</div>
</template>
