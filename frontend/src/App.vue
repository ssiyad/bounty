<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Topbar from "./components/Topbar.vue";
import Banner from "./components/Banner.vue";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen flex flex-col overflow-hidden">
			<Topbar />
			<Banner
				message="This is a work in progress. You may encounter rough edges."
				variant="info"
			/>
			<RouterView />
		</div>
	</FrappeUIProvider>
</template>
