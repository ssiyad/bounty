<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Sidebar from "./components/Sidebar.vue";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen">
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
