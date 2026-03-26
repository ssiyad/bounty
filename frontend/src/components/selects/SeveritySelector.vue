<script setup lang="ts">
import { computed } from "vue";
import { Select, SelectProps, createResource } from "frappe-ui";

const model = defineModel<string>();

const props = defineProps<Omit<SelectProps, "modelValue">>();

const severities = createResource({
	url: "security.api.severity.get_severities",
	auto: true,
	cache: ["severities"],
	initialData: [],
});

const current = computed(() => severities.data.find((s: any) => s.value === model.value));
</script>

<template>
	<Select
		v-model="model"
		v-bind="props"
		class="w-max"
		placeholder="Severity"
		:options="severities.data"
	>
		<template v-if="current" #prefix>
			<div
				class="size-2 rounded-full"
				:class="{
					'bg-surface-gray-5': current?.color == 'gray',
					'bg-surface-red-5': current?.color == 'red',
					'bg-red-400': current?.color == 'orange',
					'bg-surface-green-3': current?.color == 'green',
					'bg-surface-blue-3': current?.color == 'blue',
				}"
			/>
		</template>
		<template #option="{ option }">
			<div class="inline-flex gap-2 items-center">
				<div
					class="size-2 rounded-full"
					:class="{
						'bg-surface-gray-5': option.color == 'gray',
						'bg-surface-red-5': option.color == 'red',
						'bg-red-400': option.color == 'orange',
						'bg-surface-green-3': option.color == 'green',
						'bg-surface-blue-3': option.color == 'blue',
					}"
				/>
				{{ option.label }}
			</div>
		</template>
	</Select>
</template>
