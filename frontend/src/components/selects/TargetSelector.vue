<script setup lang="ts">
import { Select, type SelectProps, createResource } from "frappe-ui";

interface Target {
	name: string;
	title: string;
}

interface Option {
	value: string;
	label: string;
}

const model = defineModel<string>();

const props = defineProps<Omit<SelectProps, "modelValue">>();

const targets = createResource({
	url: "security.api.target.get_targets",
	auto: true,
	cache: ["targets"],
	initialData: [] as Option[],
	transform: (data: Target[]) => {
		const d = data.map((t) => ({
			value: t.name,
			label: t.title,
		}));
		d.unshift({ value: "_", label: "Any" });
		return d;
	},
});
</script>

<template>
	<Select
		:model-value="model"
		@update:model-value="$emit('update:modelValue', $event === '_' ? '' : $event)"
		v-bind="props"
		class="w-max"
		placeholder="Target"
		:options="targets.data"
	>
		<template v-if="model" #prefix>
			<Target v-if="model !== '_'" :target="model" variant="logo" />
		</template>
		<template #option="{ option }">
			<div v-if="option.value === '_'" class="ml-5">{{ option.label }}</div>
			<Target v-else :target="option.value" />
		</template>
	</Select>
</template>
