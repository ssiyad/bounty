<script setup lang="ts">
import { Badge, type BadgeProps } from "frappe-ui";
import { computed } from "vue";

const props = defineProps<
	BadgeProps & {
		severity: string;
	}
>();

const theme = computed(() => {
	switch (props.severity) {
		case "Informational":
			return "gray";
		case "Low":
			return "green";
		case "Medium":
			return "blue";
		case "High":
			return "orange";
		case "Critical":
			return "red";
		default:
			return "gray";
	}
});
</script>

<template>
	<Badge v-bind="props" :label="severity" :theme="theme" />
</template>
