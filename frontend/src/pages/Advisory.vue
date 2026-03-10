<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Badge, createResource } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "../utils/badgeThemes";
import Target from "../components/Target.vue";
import PageLayout from "../layouts/PageLayout.vue";

const route = useRoute();
const id = route.params.id as string;

const advisory = createResource({
	url: "bounty.api.advisory.get_advisory",
	auto: true,
	cache: ["advisory", id],
	makeParams: () => ({
		name: id,
	}),
});

const breadcrumbs = computed(() => [
	{
		label: "Advisories",
		route: {
			name: "Advisories",
		},
	},
	{
		label: advisory.data?.frappe_reference,
	},
]);
</script>

<template>
	<PageLayout :breadcrumbs="breadcrumbs">
		<div v-if="advisory.data" class="mx-auto container py-12">
			<div class="max-w-3xl mx-auto">
				<span class="font-mono text-xs text-ink-gray-4">
					{{ advisory.data.frappe_reference }}
				</span>
				<h1 class="mt-2 text-2xl font-semibold text-ink-gray-9 leading-relaxed">
					{{ advisory.data.title }}
				</h1>
				<div class="mt-4 flex flex-wrap items-center gap-2 text-sm text-ink-gray-5">
					<Badge
						:label="advisory.data.severity"
						:theme="severityTheme(advisory.data.severity)"
					/>
					<span class="text-ink-gray-4">&middot;</span>
					<span class="font-medium text-ink-gray-7">{{
						advisory.data.reported_by
					}}</span>
					<span class="text-ink-gray-4">&middot;</span>
					<Target :target="advisory.data.target" />
					<span class="text-ink-gray-4">&middot;</span>
					<span>{{ formatDate(advisory.data.published_on, "PPP") }}</span>
				</div>
				<div
					v-if="advisory.data.cve || advisory.data.github_reference"
					class="mt-4 flex flex-wrap items-center gap-4 text-sm"
				>
					<a
						v-if="advisory.data.cve"
						:href="`https://cve.mitre.org/cgi-bin/cvename.cgi?name=${advisory.data.cve}`"
						target="_blank"
						rel="noopener"
						class="inline-flex items-center gap-1.5 text-ink-gray-7 hover:text-ink-gray-9 transition-colors"
					>
						<svg
							class="size-4"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
						</svg>
						{{ advisory.data.cve }}
					</a>
					<a
						v-if="advisory.data.github_reference"
						:href="advisory.data.github_reference"
						target="_blank"
						rel="noopener"
						class="inline-flex items-center gap-1.5 text-ink-gray-7 hover:text-ink-gray-9 transition-colors"
					>
						<svg class="size-4" viewBox="0 0 24 24" fill="currentColor">
							<path
								d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"
							/>
						</svg>
						GitHub
					</a>
				</div>
				<hr class="mt-6 mb-6" />
				<div class="text-base leading-relaxed text-ink-gray-8 whitespace-pre-line">
					{{ advisory.data.content }}
				</div>
			</div>
		</div>
	</PageLayout>
</template>
