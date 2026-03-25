<script setup lang="ts">
import { computed } from "vue";
import { Select, SelectProps, SelectableOption, createResource } from "frappe-ui";

const model = defineModel<string>();

const props = defineProps<Omit<SelectProps, "modelValue">>();

const targets = createResource({
	url: "security.api.target.get_targets",
	auto: true,
	cache: ["targets"],
	initialData: [],
});

const options = computed(() => {
	const _: SelectableOption[] = targets.data.map((target: any) => ({
		label: target.title,
		value: target.name,
	}));
	_.unshift({ label: "", value: "" });
	return _;
});
</script>

<template>
	<Select v-model="model" v-bind="props" class="w-max" placeholder="Target" :options="options">
		<template #option="{ option }">
			<Target :target="option.value" />
		</template>
	</Select>
</template>
