<script setup lang="ts">
import { Breadcrumbs, type BreadcrumbsProps, Button } from "frappe-ui";
import { session } from "@/data/session";

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
			<div id="topbar-actions" />
			<a v-if="!session.isLoggedIn" href="/login">
				<Button label="Login" icon-left="log-in" variant="solid" />
			</a>
		</div>
	</div>
</template>
