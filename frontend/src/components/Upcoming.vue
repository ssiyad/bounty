<script setup lang="ts">
import { Button } from "frappe-ui";
import ConstructionIcon from "~icons/lucide/construction";
</script>

<template>
	<div class="size-full flex flex-col gap-4 items-center justify-center text-center">
		<ConstructionIcon class="text-ink-gray-7 size-12" />
		<p class="text-ink-gray-7 text-sm">Work in progress. Please check back later.</p>
		<Button label="Report an Issue" variant="subtle" icon-right="external-link" />
	</div>
</template>
