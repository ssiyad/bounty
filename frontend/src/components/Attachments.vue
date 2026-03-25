<script setup lang="ts">
import { Button, FileUploader, createListResource } from "frappe-ui";
import UploadIcon from "~icons/lucide/upload";

const props = defineProps<{
	doctype: string;
	docname: string;
}>();

const attachments = createListResource({
	doctype: "File",
	auto: true,
	filters: {
		attached_to_doctype: props.doctype,
		attached_to_name: props.docname,
	},
	fields: ["name", "file_name", "file_url"],
	initialData: [],
});
</script>

<template>
	<div class="space-y-2">
		<div class="flex items-center justify-between">
			<div class="text-sm font-medium">Attachments</div>
			<FileUploader
				:fileTypes="['image/*']"
				:upload-args="{
					doctype: 'FS Draft',
					docname: docname,
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
			class="group flex items-center justify-between"
		>
			<a :href="attachment.file_url" target="_blank">
				<div class="text-sm text-ink-gray-8 hover:text-ink-gray-9">
					{{ attachment.file_name }}
				</div>
			</a>
			<Button
				class="opacity-0 group-hover:opacity-100"
				label="Upload"
				variant="ghost"
				icon="x"
			/>
		</div>
	</div>
</template>
