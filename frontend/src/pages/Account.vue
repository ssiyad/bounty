<script setup lang="ts">
import { Button, usePageMeta } from "frappe-ui";
import { hunterResource } from "../data/hunter";
import { session } from "../data/session";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Account"),
}));
</script>

<template>
	<div class="container mx-auto py-8 overflow-y-auto">
		<div>
			<div class="text-3xl font-medium mb-4">
				Hello, {{ hunterResource.data?.display_name }}
			</div>
			<Button
				label="Logout"
				variant="solid"
				icon-left="log-out"
				@click="session.logout.submit()"
			/>
		</div>
	</div>
</template>
