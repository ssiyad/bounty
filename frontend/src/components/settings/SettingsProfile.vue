<script setup lang="ts">
import { Button, Textarea, TextInput, createDocumentResource } from "frappe-ui";
import { session } from "../../data/session";

const hunter = createDocumentResource({
	doctype: "Bounty Hunter",
	name: session.user!,
	auto: true,
});
</script>

<template>
	<div class="h-full overflow-y-auto p-4">
		<div class="flex items-center justify-between mb-6">
			<p class="text-lg font-medium">Profile</p>
			<Button
				label="Save"
				variant="solid"
				icon-left="save"
				:loading="hunter.save.loading"
				@click="hunter.save.submit(hunter.doc)"
			/>
		</div>
		<div v-if="hunter.doc" class="space-y-4">
			<div class="space-y-2">
				<p class="font-medium">Bio</p>
				<Textarea
					v-model="hunter.doc.bio"
					placeholder="Tell us a little bit about yourself."
				/>
			</div>
			<div class="space-y-2">
				<p class="font-medium">GitHub</p>
				<TextInput v-model="hunter.doc.social_github" type="text" />
				<p class="text-xs">Link to your GitHub account.</p>
			</div>
			<div class="space-y-2">
				<p class="font-medium">LinkedIn</p>
				<TextInput v-model="hunter.doc.social_linkedin" type="text" />
				<p class="text-xs">Link to your LinkedIn account.</p>
			</div>
			<div class="space-y-2">
				<p class="font-medium">Company</p>
				<TextInput v-model="hunter.doc.company" type="text" />
			</div>
			<div class="space-y-2">
				<p class="font-medium">Location</p>
				<TextInput v-model="hunter.doc.location" type="text" />
			</div>
		</div>
	</div>
</template>
