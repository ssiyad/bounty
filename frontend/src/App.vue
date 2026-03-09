<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen">
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
