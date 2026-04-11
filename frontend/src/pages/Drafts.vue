<script setup lang="ts">
import DraftListItem from "@/components/list/DraftListItem.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { Button, createListResource } from "frappe-ui";

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
			}"
		>
			<Button label="Draft" icon-left="plus" variant="solid" />
		</RouterLink>
	</Teleport>
	<div class="divide-y grow min-h-0 overflow-y-auto">
		<!-- Desktop table header -->
		<div class="hidden md:flex h-12 px-5 py-4 font-medium bg-surface-gray-1">
			<div class="grow">Title</div>
			<div class="w-[150px] text-end">Updated</div>
		</div>
		<DraftListItem
			v-for="draft in drafts.data"
			:key="draft.name"
			:draft="draft"
		/>
	</div>
	<div class="h-12 shrink-0 flex items-center justify-end px-4 md:px-5 border-t">
		<Button
			label="Load More"
			:loading="drafts.loading"
			:disabled="!drafts.hasNextPage"
			@click="drafts.next()"
		/>
	</div>
</template>