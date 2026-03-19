<script setup lang="ts">
import { computed, watchEffect } from "vue";
import { useRoute } from "vue-router";
import { Badge, Button, createResource } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "@/utils/badgeThemes";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Target from "@/components/Target.vue";
import DateIcon from "~icons/lucide/calendar";
import ReferenceIcon from "~icons/lucide/globe";
import UserIcon from "~icons/lucide/user";

const route = useRoute();
const id = route.params.id as string;

const advisory = createResource({
	url: "bounty.api.advisory.get_advisory",
	auto: true,
	cache: ["advisory", id],
	makeParams: () => ({
		name: id,
	}),
	onSuccess: () => target.fetch(),
});

const target = createResource({
	url: "bounty.api.target.get_target",
	cache: ["target", advisory.data?.target],
	makeParams: () => ({
		name: advisory.data?.target,
	}),
});

const { set } = useBreadcrumbs();

watchEffect(() => {
	set([
		{
			label: "Advisories",
			route: { name: "Advisories" },
		},
		{
			label: advisory.data?.frappe_reference ?? id,
		},
	]);
});

const gitHubUrl = computed(() => {
	const repository = target.data?.repository;
	const reference = advisory.data?.github_reference;
	if (repository && reference) {
		return `${repository}/security/advisories/${reference}`;
	}
});
</script>

<template>
	<Teleport defer to="#topbar-actions">
		<a v-if="gitHubUrl" :href="gitHubUrl" target="_blank">
			<Button label="GitHub" icon-left="github" />
		</a>
	</Teleport>
	<div class="overflow-y-auto">
		<div v-if="advisory.data" class="py-14 max-w-[840px] mx-auto">
			<h1 class="mb-4 text-3xl font-semibold text-ink-gray-9 leading-relaxed">
				{{ advisory.data.title }}
			</h1>
			<div class="flex flex-wrap items-center gap-2 text-sm text-ink-gray-5">
				<div class="flex items-center gap-1">
					<ReferenceIcon class="size-4" />
					<div class="font-mono text-xs text-ink-gray-7">
						{{ advisory.data.frappe_reference }}
					</div>
				</div>
				<div class="text-ink-gray-4">&mdash;</div>
				<Badge
					:label="advisory.data.severity"
					:theme="severityTheme(advisory.data.severity)"
				/>
				<div class="text-ink-gray-4">&mdash;</div>
				<Target class="text-ink-gray-7" :target="advisory.data.target" />
				<div class="text-ink-gray-4">&mdash;</div>
				<div class="flex items-center gap-1">
					<DateIcon class="size-4" />
					<div class="text-ink-gray-7">
						{{ formatDate(advisory.data.published_on, "PPP") }}
					</div>
				</div>
				<template v-if="advisory.data.reported_by">
					<div class="text-ink-gray-4">&mdash;</div>
					<div class="flex items-center gap-1">
						<UserIcon class="size-4" />
						<div class="font-medium text-ink-gray-7">
							{{ advisory.data.reported_by }}
						</div>
					</div>
				</template>
			</div>
			<hr class="mt-6 mb-6" />
			<div
				v-html="advisory.data.content"
				class="prose prose-sm max-w-none leading-relaxed mb-8"
			/>
		</div>
	</div>
</template>
