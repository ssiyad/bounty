<script setup lang="ts">
import Target from "@/components/Target.vue";
import { severityTheme } from "@/utils/badgeThemes";
import { formatDate } from "date-fns";
import { Badge } from "frappe-ui";
import DateIcon from "~icons/lucide/calendar";
import ReferenceIcon from "~icons/lucide/globe";
import UserIcon from "~icons/lucide/user";

defineProps<{
	advisory: {
		name: string;
		title: string;
		frappe_reference: string;
		severity: string;
		target: string;
		published_on: string;
		reported_by?: string;
	};
}>();
</script>

<template>
	<RouterLink
		:to="{
			name: 'Advisory',
			params: {
				id: advisory.name,
			},
		}"
		class="block"
	>
		<!-- Mobile card layout -->
		<div class="md:hidden flex">
			<div
				class="w-1 shrink-0 rounded-l"
				:class="{
					'bg-surface-gray-2 ': advisory.severity === 'Informational',
					'bg-surface-red-2': advisory.severity === 'Critical',
					'bg-surface-amber-1': advisory.severity === 'High',
					'bg-surface-blue-2': advisory.severity === 'Medium',
					'bg-surface-green-2': advisory.severity === 'Low',
				}"
			/>
			<div class="grow min-w-0 border rounded-r px-3 py-3">
				<div class="truncate font-medium mb-4">{{ advisory.title }}</div>
				<div class="flex flex-wrap gap-3 text-xs text-ink-gray-7 mb-3">
					<div class="flex gap-1 items-center">
						<ReferenceIcon class="size-3.5" />
						<div class="font-mono">{{ advisory.frappe_reference }}</div>
					</div>
					<div class="flex gap-1 items-center">
						<DateIcon class="size-3.5" />
						<div>{{ formatDate(advisory.published_on, "PP") }}</div>
					</div>
					<template v-if="advisory.reported_by">
						<div class="flex gap-1 items-center">
							<UserIcon class="size-3.5" />
							<div>{{ advisory.reported_by }}</div>
						</div>
					</template>
				</div>
				<div class="flex items-center gap-2">
					<Badge
						:label="advisory.severity"
						:theme="severityTheme(advisory.severity)"
					/>
					<Target class="text-ink-gray-7 text-xs" :target="advisory.target" />
				</div>
			</div>
		</div>
		<!-- Desktop row layout -->
		<div class="hidden md:flex h-20">
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
</template>
