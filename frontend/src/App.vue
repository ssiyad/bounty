<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Topbar from "./components/Topbar.vue";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen flex flex-col overflow-hidden">
			<Topbar />
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
