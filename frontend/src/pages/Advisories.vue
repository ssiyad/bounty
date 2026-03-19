<script setup lang="ts">
import { ref, watch } from "vue";
import { Badge, Button, Select, Switch, createResource } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "@/utils/badgeThemes";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Target from "@/components/Target.vue";
import DateIcon from "~icons/lucide/calendar";
import ReferenceIcon from "~icons/lucide/globe";
import UserIcon from "~icons/lucide/user";

useBreadcrumbs().set([{ label: "Advisories" }]);

const target = ref("");
const severity = ref("");
const myReports = ref(false);

const targets = createResource({
	url: "bounty.api.target.get_targets",
	auto: true,
	cache: ["targets"],
});

const severities = createResource({
	url: "bounty.api.severity.get_severities",
	auto: true,
	cache: ["severities"],
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
	<div class="mx-auto max-w-[840] py-14">
		<div class="text-3xl font-semibold mb-6">Advisories</div>
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
		<div class="flex flex-col gap-4">
			<RouterLink
				v-for="advisory in advisories.data"
				:key="advisory.name"
				:to="{
					name: 'Advisory',
					params: {
						id: advisory.name,
					},
				}"
			>
				<div class="h-20 flex">
					<div
						class="w-1 shrink-0 rounded-l h-full"
						:class="{
							'bg-surface-gray-2 ': advisory.severity === 'Informational',
							'bg-surface-red-2': advisory.severity === 'Critical',
							'bg-surface-amber-1': advisory.severity === 'High',
							'bg-surface-blue-2': advisory.severity === 'Medium',
							'bg-surface-green-2': advisory.severity === 'Low',
						}"
					/>
					<div class="grow border-y border-r rounded-r px-5 flex items-center gap-2">
						<div class="flex flex-col gap-3 min-w-0 grow">
							<div class="truncate">{{ advisory.title }}</div>
							<div class="flex gap-2 items-center">
								<div
									class="flex gap-1 items-center font-mono text-xs text-ink-gray-5"
								>
									<ReferenceIcon class="size-4" />
									{{ advisory.frappe_reference }}
								</div>
								<div class="text-ink-gray-2">&mdash;</div>
								<div class="flex gap-1 items-center text-xs text-ink-gray-5">
									<DateIcon class="size-4" />
									<div>{{ formatDate(advisory.published_on, "PPP") }}</div>
								</div>
								<div v-if="advisory.reported_by" class="text-ink-gray-2">
									&mdash;
								</div>
								<div
									v-if="advisory.reported_by"
									class="flex gap-1 items-center text-xs text-ink-gray-5"
								>
									<UserIcon class="size-4" />
									<div>{{ advisory.reported_by }}</div>
								</div>
							</div>
						</div>
						<div>
							<Badge
								:label="advisory.severity"
								:theme="severityTheme(advisory.severity)"
							/>
						</div>
						<div class="text-ink-gray-2">&mdash;</div>
						<div><Target :target="advisory.target" /></div>
					</div>
				</div>
			</RouterLink>
		</div>
	</div>
</template>
