<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-dvh w-dvw md:h-screen md:w-screen">
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
