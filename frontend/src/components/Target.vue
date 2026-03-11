<script setup lang="ts">
import { Avatar, createResource } from "frappe-ui";

const props = withDefaults(
	defineProps<{
		target?: string;
	}>(),
	{
		target: "",
	},
);

const target = createResource({
	url: "bounty.api.target.get_target",
	auto: !!props.target,
	cache: ["target", props.target],
	initialData: {
		name: props.target,
		title: props.target,
		logo: "",
		repository: "",
	},
	makeParams: () => ({
		name: props.target,
	}),
});
</script>

<template>
	<div class="w-max">
		<div class="flex items-center gap-2">
			<img
				v-if="target.data.logo"
				class="flex size-4 items-center justify-center rounded-[5px]"
				:src="target.data.logo"
				:alt="target.data.title"
			/>
			<Avatar v-else :label="target.data.title" shape="square" size="xs" />
			<div>
				{{ target.data.title }}
			</div>
		</div>
	</div>
</template>
