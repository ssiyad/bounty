<script setup lang="ts">
import { computed } from "vue";
import { Avatar } from "frappe-ui";
import { session } from "../data/session";
import { hunterResource } from "../data/hunter";

const hunter = computed(() => {
	if (session.isLoggedIn && hunterResource.data) {
		return hunterResource.data.display_name;
	}
	return "Hunter";
});
</script>

<template>
	<div class="flex items-center gap-2">
		<Avatar :label="hunter" size="lg" />
		<p class="font-medium">
			{{ hunter }}
		</p>
	</div>
</template>
