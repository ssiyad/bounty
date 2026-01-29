<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Breadcrumbs } from "frappe-ui";

const route = useRoute();

const breadcrumbs = computed(() => {
	return route.matched
		.filter((r) => r.meta?.breadcrumb)
		.map((r) => ({
			label:
				typeof r.meta.breadcrumb === "function"
					? r.meta.breadcrumb(route)
					: r.meta.breadcrumb,
			route: r.path,
		}));
});
</script>

<template>
	<Breadcrumbs :items="breadcrumbs" />
</template>
