<script setup lang="ts">
import { Button, Textarea, TextInput, usePageMeta } from "frappe-ui";
import { hunterResource, hunterSaveResource } from "../../data/hunter";
// import { session } from "../data/session";
// import { pageTitle } from "../utils/page";

// usePageMeta(() => ({
// 	title: pageTitle("Account"),
// }));

// function toggleTheme() {
// 	const currentTheme = document.documentElement.getAttribute("data-theme");
// 	const newTheme = currentTheme === "dark" ? "light" : "dark";
// 	document.documentElement.setAttribute("data-theme", newTheme);
// }
</script>

<template>
	<div class="overflow-y-auto">
		<div class="">
			<div class="max-w-md space-y-6">
				<div class="space-y-2">
					<p class="font-medium">Bio</p>
					<Textarea
						v-model="hunterResource.data.bio"
						placeholder="Tell us a little bit about yourself."
					/>
				</div>
				<div class="space-y-2">
					<p class="font-medium">GitHub</p>
					<TextInput v-model="hunterResource.data.social_github" type="text" />
					<p class="text-xs">Link to your GitHub account.</p>
				</div>
				<div class="space-y-2">
					<p class="font-medium">LinkedIn</p>
					<TextInput v-model="hunterResource.data.social_linkedin" type="text" />
					<p class="text-xs">Link to your LinkedIn account.</p>
				</div>
				<div class="space-y-2">
					<p class="font-medium">Company</p>
					<TextInput v-model="hunterResource.data.company" type="text" />
				</div>
				<div class="space-y-2">
					<p class="font-medium">Location</p>
					<TextInput v-model="hunterResource.data.location" type="text" />
				</div>
				<Button
					label="Save"
					variant="solid"
					icon-left="save"
					@click="hunterSaveResource.submit(hunterResource.data)"
				/>
			</div>
		</div>
	</div>
</template>
