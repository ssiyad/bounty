<script setup lang="ts">
import { Button, Textarea, TextInput, usePageMeta } from "frappe-ui";
import { hunterResource } from "../data/hunter";
import { session } from "../data/session";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Account"),
}));
</script>

<template>
	<div class="overflow-y-auto">
		<div class="container mx-auto py-8">
			<div class="mb-8 flex items-center justify-between">
				<div class="space-y-1">
					<p class="text-3xl font-semibold">
						Hello, {{ hunterResource.data?.display_name }}
					</p>
					<p class="text-xl font-semibold text-ink-gray-7">
						{{ hunterResource.data?.user_id }}
					</p>
				</div>
				<Button
					label="Logout"
					variant="subtle"
					theme="red"
					icon-left="log-out"
					@click="session.logout.submit()"
				/>
			</div>
			<div class="max-w-md space-y-6">
				<div class="space-y-2">
					<p class="font-medium">Bio</p>
					<Textarea placeholder="Tell us a little bit about yourself." />
				</div>
				<div class="space-y-2">
					<p class="font-medium">GitHub</p>
					<TextInput type="text" />
					<p class="text-xs">Link to your GitHub account.</p>
				</div>
				<div class="space-y-2">
					<p class="font-medium">LinkedIn</p>
					<TextInput type="text" />
					<p class="text-xs">Link to your LinkedIn account.</p>
				</div>
				<div class="space-y-2">
					<p class="font-medium">Company</p>
					<TextInput type="text" />
				</div>
				<div class="space-y-2">
					<p class="font-medium">Location</p>
					<TextInput type="text" />
				</div>
				<Button label="Save" variant="solid" icon-left="save" />
			</div>
		</div>
	</div>
</template>
