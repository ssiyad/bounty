<script setup lang="ts">
import TopbarBreadcrumbs from "./TopbarBreadcrumbs.vue";
</script>

<template>
	<div class="px-4 py-3 flex items-center justify-between border-b">
		<TopbarBreadcrumbs />
		<div class="flex items-center gap-2">
			<slot />
		</div>
	</div>
</template>
