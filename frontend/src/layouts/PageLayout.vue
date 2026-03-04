<script setup lang="ts">
import Banner from "../components/Banner.vue";
import Topbar from "../components/Topbar.vue";
</script>

<template>
	<div>
		<Topbar>
			<slot name="actions" />
		</Topbar>
		<Banner
			message="This is a work in progress. You may encounter rough edges."
			variant="warning"
		/>
		<slot />
	</div>
</template>
