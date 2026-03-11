<script setup lang="ts">
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import UpcomingPlaceholder from "@/components/UpcomingPlaceholder.vue";

useBreadcrumbs().reset();
</script>

<template>
	<UpcomingPlaceholder />
</template>
