<script setup lang="ts">
import { type BreadcrumbsProps, Button } from "frappe-ui";
import Banner from "../components/Banner.vue";
import SidebarPublic from "../components/SidebarPublic.vue";
import Topbar from "../components/Topbar.vue";

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
	<div class="size-full flex overflow-hidden">
		<SidebarPublic />
		<div class="flex flex-col overflow-hidden grow">
			<Topbar v-if="breadcrumbs.length" :breadcrumbs="breadcrumbs">
				<slot name="actions" />
			</Topbar>
			<Banner
				message="This is a work in progress. You may encounter rough edges."
				variant="warning"
			>
				<a href="https://github.com/ssiyad/bounty/issues" target="_blank" rel="noopener">
					<Button label="Report an Issue" variant="ghost" icon-right="external-link" />
				</a>
			</Banner>
			<slot />
		</div>
	</div>
</template>
