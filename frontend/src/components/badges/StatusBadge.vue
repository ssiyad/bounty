<script setup lang="ts">
import { Badge, BadgeProps } from "frappe-ui";
import { computed } from "vue";

const props = defineProps<
	BadgeProps & {
		status: string;
	}
>();

const theme = computed(() => {
	switch (props.status) {
		case "Accepted":
			return "green";
		case "Rejected":
			return "red";
		case "Pending":
			return "orange";
		default:
			return "gray";
	}
});
</script>

<template>
	<Badge v-bind="props" :label="status" :theme="theme" />
</template>
