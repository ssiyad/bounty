<script setup lang="ts">
import { formatDate } from "date-fns";
import { Button, createListResource } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";

useBreadcrumbs().set([{ label: "Drafts" }]);

const drafts = createListResource({
	doctype: "FS Draft",
	auto: true,
	fields: ["name", "title", "modified"],
	orderBy: "modified desc",
});
</script>

<template>
	<Teleport defer to="#topbar-actions">
		<RouterLink
			:to="{
				name: 'Draft',
				params: {
					id: 'new-report',
				},
			}"
		>
			<Button label="Draft" icon-left="plus" variant="solid" />
		</RouterLink>
	</Teleport>
	<div class="divide-y">
		<div class="flex h-12 px-5 py-4 font-medium bg-surface-gray-1">
			<div class="grow">Title</div>
			<div class="w-[150px] text-end">Updated</div>
		</div>
		<RouterLink
			v-for="draft in drafts.data"
			:key="draft.name"
			:to="{
				name: 'Draft',
				params: {
					id: draft.name,
				},
			}"
			class="block"
		>
			<div class="flex h-12 px-5 py-4 cursor-pointer">
				<div class="grow">{{ draft.title }}</div>
				<div class="w-[150px] text-end">
					{{ formatDate(draft.modified, "PPP") }}
				</div>
			</div>
		</RouterLink>
	</div>
</template>
