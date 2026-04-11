<script setup lang="ts">
import ComingSoon from "@/components/ui/ComingSoon.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";

useBreadcrumbs().reset();
</script>

<template>
	<ComingSoon />
</template>
