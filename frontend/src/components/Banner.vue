<script setup lang="ts">
withDefaults(
	defineProps<{
		message: string;
		variant?: "default" | "info" | "warning" | "error" | "success";
	}>(),
	{
		variant: "default",
	},
);
</script>

<template>
	<div
		class="h-12 shrink-0 px-5 border-b flex items-center justify-between"
		:class="{
			'bg-surface-gray-1 text-ink-gray-9': variant === 'default',
			'bg-surface-blue-1 text-ink-blue-3': variant === 'info',
			'bg-surface-orange-1 text-ink-red-4': variant === 'warning',
			'bg-surface-red-1 text-ink-red-4': variant === 'error',
			'bg-surface-green-1 text-ink-green-3': variant === 'success',
		}"
	>
		<p class="leading-relaxed">
			{{ message }}
		</p>
		<slot />
	</div>
</template>
