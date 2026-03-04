<script setup lang="ts">
import Banner from "../components/Banner.vue";
import Sidebar from "../components/Sidebar.vue";
import Topbar from "../components/Topbar.vue";
</script>

<template>
	<div class="size-full flex overflow-hidden">
		<Sidebar />
		<div class="flex flex-col overflow-hidden grow">
			<Topbar>
				<slot name="actions" />
			</Topbar>
			<Banner
				message="This is a work in progress. You may encounter rough edges."
				variant="warning"
			/>
			<slot />
		</div>
	</div>
</template>
