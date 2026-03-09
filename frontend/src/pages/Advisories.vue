<script setup lang="ts">
import { ref, watch } from "vue";
import { Badge, Select, createResource, createListResource } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "../utils/badgeThemes";
import Target from "../components/Target.vue";

const target = ref("");
const severity = ref("");

const targets = createListResource({
	doctype: "Bounty Target",
	auto: true,
	cache: true,
	fields: ["name", "title"],
});

const severities = createResource({
	url: "bounty.api.severity.get_severities",
	auto: true,
	cache: true,
});

const advisories = createResource({
	url: "bounty.api.advisory.get_advisories",
	auto: true,
	makeParams: () => ({
		target: target.value,
		severity: severity.value,
	}),
});

watch([target, severity], () => advisories.fetch());
</script>

<template>
	<div class="mx-auto container py-12">
		<div class="mb-8">
			<h1 class="text-2xl font-semibold text-ink-gray-9">Security Advisories</h1>
			<p class="mt-2 text-base text-ink-gray-6">
				Public disclosure of security vulnerabilities found in Frappe products.
			</p>
		</div>
		<div class="mb-4 flex flex-wrap gap-3">
			<Select
				v-model="target"
				class="w-max"
				placeholder="Target"
				:options="
					targets.data?.map((target) => ({
						label: target.title,
						value: target.name,
					}))
				"
			>
				<template #option="{ option }">
					<Target :target="option.value" />
				</template>
			</Select>
			<Select
				v-model="severity"
				class="w-max"
				placeholder="Severity"
				:options="severities.data"
			>
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
						></div>
						{{ option.label }}
					</div>
				</template>
			</Select>
		</div>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
			<div
				v-for="advisory in advisories.data"
				:key="advisory.name"
				class="flex flex-col justify-between rounded-lg border p-5"
			>
				<div>
					<div class="mb-3 flex items-center justify-between">
						<span class="font-mono text-sm text-ink-gray-5">
							{{ advisory.frappe_reference }}
						</span>
						<Badge
							:label="advisory.severity"
							:theme="severityTheme(advisory.severity)"
						/>
					</div>
					<p class="text-base font-medium text-ink-gray-9">
						{{ advisory.title }}
					</p>
				</div>
				<div class="mt-4 flex items-center justify-between">
					<Target :target="advisory.target" />
					<span class="text-sm text-ink-gray-5">
						{{ formatDate(advisory.published_on, "PPP") }}
					</span>
				</div>
			</div>
		</div>
	</div>
</template>
