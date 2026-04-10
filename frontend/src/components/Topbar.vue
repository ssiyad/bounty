<script setup lang="ts">
import { session } from "@/data/session";
import { Breadcrumbs, type BreadcrumbsProps, Button } from "frappe-ui";

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
	<div class="h-12 shrink-0 px-4 md:px-5 flex items-center justify-between border-b">
		<div class="min-w-0 flex-1">
			<Breadcrumbs :items="breadcrumbs" class="truncate" />
		</div>
		<div class="flex items-center gap-2 shrink-0">
			<div id="topbar-actions" class="flex items-center gap-2" />
			<a v-if="!session.isLoggedIn" href="/login">
				<Button label="Login" icon-left="log-in" variant="solid" class="h-9" />
			</a>
		</div>
	</div>
</template>
