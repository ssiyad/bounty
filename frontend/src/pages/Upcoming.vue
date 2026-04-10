<script setup lang="ts">
import UpcomingPlaceholder from "@/components/UpcomingPlaceholder.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";

useBreadcrumbs().reset();
</script>

<template>
	<UpcomingPlaceholder />
</template>
