<script setup lang="ts">
import { Avatar, createDocumentResource } from "frappe-ui";

const props = withDefaults(
	defineProps<{
		target?: string;
	}>(),
	{
		target: "",
	},
);

const target = createDocumentResource({
	doctype: "Bounty Target",
	name: props.target,
	cache: ["Bounty Target", props.target],
	auto: !!props.target,
});
</script>

<template>
	<a v-if="target.doc" :href="target.doc.repository" target="_blank" class="block w-max">
		<div class="flex items-center gap-2">
			<img
				v-if="target.doc.logo"
				class="flex size-6 items-center justify-center rounded-[5px]"
				:src="target.doc.logo"
				:alt="target.doc.name"
			/>
			<Avatar v-else :label="target.name" shape="square" />
			<div class="font-medium">
				{{ target.doc.name }}
			</div>
		</div>
	</a>
</template>
