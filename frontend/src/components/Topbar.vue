<script setup lang="ts">
import { Breadcrumbs, BreadcrumbsProps } from "frappe-ui";

withDefaults(
	defineProps<{
		breadcrumbs?: BreadcrumbsProps["items"];
	}>(),
	{
		breadcrumbs: () => [],
	},
);
</script>

<template>
	<div class="h-12.5 px-4 py-3 flex items-center justify-between border-b">
		<Breadcrumbs :items="breadcrumbs" />
		<div class="flex items-center gap-2">
			<slot />
		</div>
	</div>
</template>
