<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Topbar from "./components/Topbar.vue";
</script>

<template>
	<FrappeUIProvider>
		<div>
			<Topbar />
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
