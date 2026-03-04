<script setup lang="ts">
import { FrappeUIProvider } from "frappe-ui";
import Sidebar from "./components/Sidebar.vue";
import Topbar from "./components/Topbar.vue";
import Banner from "./components/Banner.vue";
</script>

<template>
	<FrappeUIProvider>
		<div class="h-screen w-screen flex overflow-hidden">
			<Sidebar />
			<div class="flex flex-col overflow-hidden grow">
				<Topbar />
				<Banner
					message="This is a work in progress. You may encounter rough edges."
					variant="info"
				/>
				<RouterView />
			</div>
		</div>
	</FrappeUIProvider>
</template>
