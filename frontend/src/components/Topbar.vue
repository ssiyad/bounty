<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Button } from "frappe-ui";
import TopbarAccount from "./TopbarAccount.vue";
import TopbarBreadcrumbs from "./TopbarBreadcrumbs.vue";

const route = useRoute();
const isHome = computed(() => route.path === "/");
</script>

<template>
	<div class="px-4 py-3 flex items-center justify-between">
		<TopbarBreadcrumbs />
		<div class="space-x-2">
			<Button label="Help" icon-left="info" />
			<RouterLink to="/leaderboard">
				<Button label="Leaderboard" icon-left="trending-up" />
			</RouterLink>
			<RouterLink to="/attempts">
				<Button label="Attempts" icon-left="crosshair" />
			</RouterLink>
			<TopbarAccount />
			<RouterLink to="/">
				<Button label="Report" icon-left="file-text" variant="solid" :disabled="isHome" />
			</RouterLink>
		</div>
	</div>
</template>
