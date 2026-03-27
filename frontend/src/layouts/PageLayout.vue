<script setup lang="ts">
import { Button } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Banner from "@/components/Banner.vue";
import Sidebar from "@/components/Sidebar.vue";
import Topbar from "@/components/Topbar.vue";

const { breadcrumbs } = useBreadcrumbs();
</script>

<template>
	<div class="size-full flex overflow-hidden">
		<Sidebar />
		<div class="flex flex-col overflow-hidden grow">
			<Topbar v-if="breadcrumbs.length" :breadcrumbs="breadcrumbs" />
			<Banner
				message="This is a work in progress. You may encounter rough edges."
				variant="info"
			>
				<a href="https://github.com/ssiyad/security/issues" target="_blank" rel="noopener">
					<Button label="Report an Issue" variant="ghost" icon-right="external-link" />
				</a>
			</Banner>
			<RouterView />
		</div>
	</div>
</template>
