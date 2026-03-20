<script setup lang="ts">
import { Ref, ref, watch } from "vue";
import { Badge, Button, Select, createResource } from "frappe-ui";
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
const start = ref(0);
const limit = 10;

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

const a_: Ref<any[]> = ref([]);
const count = ref(0);
const hasNextPage = ref(false);
const advisories = createResource({
	url: "bounty.api.advisory.get_advisories",
	auto: true,
	makeParams: () => ({
		start: start.value,
		limit: limit,
		target: target.value,
		severity: severity.value,
	}),
	onSuccess: ([data, count_, has_next_page]: [any[], number, boolean]) => {
		a_.value.push(...data);
		count.value = count_;
		hasNextPage.value = has_next_page;
	},
});

const load = () => {
	start.value = start.value + 2;
	advisories.reload();
};

watch([target, severity], () => advisories.fetch());
</script>

<template>
	<div class="overflow-y-auto">
		<div class="mx-auto max-w-[840px] py-14 w-full">
			<h1 class="text-3xl font-semibold mb-6">Advisories</h1>
			<div class="mb-4 flex items-center">
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
			</div>
			<div class="flex flex-col gap-4">
				<RouterLink
					v-for="advisory in a_"
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
							class="w-1 shrink-0 border-l border-y rounded-l h-full"
							:class="{
								'bg-surface-gray-2 ': advisory.severity === 'Informational',
								'bg-surface-red-2': advisory.severity === 'Critical',
								'bg-surface-amber-1': advisory.severity === 'High',
								'bg-surface-blue-2': advisory.severity === 'Medium',
								'bg-surface-green-2': advisory.severity === 'Low',
							}"
						/>
						<div
							class="grow min-w-0 border-y border-r rounded-r px-5 flex items-center gap-2"
						>
							<div class="flex flex-col gap-3 min-w-0 grow">
								<div class="truncate">{{ advisory.title }}</div>
								<div class="flex gap-2 items-center text-xs text-ink-gray-7">
									<div class="flex gap-1 items-center">
										<ReferenceIcon class="size-4" />
										<div class="font-mono">
											{{ advisory.frappe_reference }}
										</div>
									</div>
									<div class="text-ink-gray-4">&mdash;</div>
									<div class="flex gap-1 items-center">
										<DateIcon class="size-4" />
										<div>
											{{ formatDate(advisory.published_on, "PPP") }}
										</div>
									</div>
									<template v-if="advisory.reported_by">
										<div class="text-ink-gray-4">&mdash;</div>
										<div class="flex gap-1 items-center">
											<UserIcon class="size-4" />
											<div>
												{{ advisory.reported_by }}
											</div>
										</div>
									</template>
								</div>
							</div>
							<div>
								<Badge
									:label="advisory.severity"
									:theme="severityTheme(advisory.severity)"
								/>
							</div>
							<div class="text-ink-gray-4">&mdash;</div>
							<div>
								<Target class="text-ink-gray-7" :target="advisory.target" />
							</div>
						</div>
					</div>
				</RouterLink>
			</div>
			<div v-if="hasNextPage" class="mt-4 text-center">
				<Button label="Load More" @click="load()" />
			</div>
		</div>
	</div>
</template>
