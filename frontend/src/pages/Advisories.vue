<script setup lang="ts">
import { ref, watch } from "vue";
import { Badge, Select, Switch, createResource, createListResource } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "../utils/badgeThemes";
import Target from "../components/Target.vue";
import PageLayoutPublic from "../layouts/PageLayoutPublic.vue";

const target = ref("");
const severity = ref("");
const myReports = ref(false);

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
		my_reports: myReports.value,
	}),
});

watch([target, severity, myReports], () => advisories.fetch());
</script>

<template>
	<PageLayoutPublic
		:breadcrumbs="[
			{
				label: 'Advisories',
			},
		]"
	>
		<div class="mx-auto container py-12">
			<div class="mb-4 flex items-center justify-between">
				<div class="space-x-2">
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
				<Switch v-model="myReports" label="My Reports" class="border" />
			</div>
			<div class="divide-y">
				<RouterLink
					v-for="advisory in advisories.data"
					class="block"
					:key="advisory.name"
					:to="{
						name: 'Advisory',
						params: {
							id: advisory.name,
						},
					}"
				>
					<div
						class="flex items-center justify-between gap-4 px-5 py-4 -mx-5 hover:rounded-md transition-colors hover:bg-surface-gray-1 cursor-pointer"
					>
						<div class="min-w-0 flex-1">
							<span class="font-mono text-xs text-ink-gray-4">
								{{ advisory.frappe_reference }}
							</span>
							<p class="mt-2 text-base font-medium text-ink-gray-9 truncate">
								{{ advisory.title }}
							</p>
							<div
								class="mt-2 flex flex-wrap items-center gap-1 text-sm text-ink-gray-5"
							>
								<Badge
									:label="advisory.severity"
									:theme="severityTheme(advisory.severity)"
								/>
								<span class="text-ink-gray-4">&middot;</span>
								<span class="font-medium text-ink-gray-7">{{
									advisory.reported_by
								}}</span>
								<span class="text-ink-gray-4">&middot;</span>
								<span>{{ formatDate(advisory.published_on, "PPP") }}</span>
							</div>
						</div>
						<Target :target="advisory.target" />
					</div>
				</RouterLink>
			</div>
		</div>
	</PageLayoutPublic>
</template>
