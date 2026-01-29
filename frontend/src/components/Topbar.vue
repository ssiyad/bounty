<script setup lang="ts">
import { Button } from "frappe-ui";
import TopbarAccount from "./TopbarAccount.vue";
import TopbarBreadcrumbs from "./TopbarBreadcrumbs.vue";
</script>

<template>
	<div class="px-4 py-3 flex items-center justify-between">
		<TopbarBreadcrumbs />
		<div class="space-x-2">
			<Button label="Help" icon-left="info" />
			<RouterLink to="/leaderboard">
				<Button label="Leaderboard" icon-left="trending-up" />
			</RouterLink>
			<Button label="Attempts" icon-left="crosshair" />
			<TopbarAccount />
		</div>
	</div>
</template>
