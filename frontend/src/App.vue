<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Sidebar from "./components/Sidebar.vue";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen flex overflow-hidden">
			<Sidebar />
			<div class="flex flex-col overflow-hidden grow">
				<RouterView />
			</div>
		</div>
	</FrappeUIProvider>
</template>
