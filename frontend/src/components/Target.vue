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
	<div class="w-max">
		<div v-if="target?.doc" class="flex items-center gap-2">
			<img
				v-if="target.doc.logo"
				class="flex size-4 items-center justify-center rounded-[5px]"
				:src="target.doc.logo"
				:alt="target.doc.title"
			/>
			<Avatar v-else :label="target.name" shape="square" size="xs" />
			<div>
				{{ target.doc.title }}
			</div>
		</div>
		<div v-else>
			{{ props.target }}
		</div>
	</div>
</template>
