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
		class="px-4 py-3 border-b"
		:class="{
			'bg-gray-100 text-gray-800': variant === 'default',
			'bg-blue-100 text-blue-800': variant === 'info',
			'bg-yellow-100 text-yellow-800': variant === 'warning',
			'bg-red-100 text-red-800': variant === 'error',
			'bg-green-100 text-green-800': variant === 'success',
		}"
	>
		<p class="leading-relaxed">
			{{ message }}
		</p>
	</div>
</template>
