<script setup lang="ts">
import { computed, ref } from "vue";
import { Badge, FormControl } from "frappe-ui";
import { formatDate } from "date-fns";
import { severityTheme } from "../utils/badgeThemes";
import Target from "../components/Target.vue";

const target = ref("");
const severity = ref("");

const allAdvisories = [
	{
		name: "SA-2026-001",
		title: "Cross-Site Scripting in Web Form",
		severity: "High",
		target: "gameplan",
		published_on: "2026-02-15",
	},
	{
		name: "SA-2026-002",
		title: "SQL Injection in Report Builder",
		severity: "Critical",
		target: "gameplan",
		published_on: "2026-02-10",
	},
	{
		name: "SA-2026-003",
		title: "Insecure Direct Object Reference in API",
		severity: "Medium",
		target: "press",
		published_on: "2026-01-28",
	},
	{
		name: "SA-2026-004",
		title: "Information Disclosure via Error Messages",
		severity: "Low",
		target: "gameplan",
		published_on: "2026-01-15",
	},
	{
		name: "SA-2026-005",
		title: "CSRF Token Bypass in Document Actions",
		severity: "High",
		target: "press",
		published_on: "2026-01-05",
	},
	{
		name: "SA-2025-018",
		title: "Privilege Escalation via Role Permissions",
		severity: "Critical",
		target: "gameplan",
		published_on: "2025-12-20",
	},
	{
		name: "SA-2025-017",
		title: "Open Redirect in Login Flow",
		severity: "Medium",
		target: "raven",
		published_on: "2025-12-10",
	},
	{
		name: "SA-2025-016",
		title: "Verbose Server Headers Disclosure",
		severity: "Informational",
		target: "gameplan",
		published_on: "2025-11-28",
	},
];

const targets = [...new Set(allAdvisories.map((a) => a.target))];
const severities = [...new Set(allAdvisories.map((a) => a.severity))];

const targetOptions = [
	{ label: "All Targets", value: "" },
	...targets.map((t) => ({ label: t, value: t })),
];
const severityOptions = [
	{ label: "All Severities", value: "" },
	...severities.map((s) => ({ label: s, value: s })),
];

const advisories = computed(() =>
	allAdvisories.filter(
		(a) =>
			(!target.value || a.target === target.value) &&
			(!severity.value || a.severity === severity.value),
	),
);
</script>

<template>
	<div class="mx-auto container py-12">
		<div class="mb-8">
			<h1 class="text-2xl font-semibold text-ink-gray-9">Security Advisories</h1>
			<p class="mt-2 text-base text-ink-gray-6">
				Public disclosure of security vulnerabilities found in Frappe products.
			</p>
		</div>
		<div class="mb-6 flex flex-wrap gap-3">
			<FormControl
				v-model="target"
				type="select"
				:options="targetOptions"
				placeholder="Target"
			/>
			<FormControl
				v-model="severity"
				type="select"
				:options="severityOptions"
				placeholder="Severity"
			/>
		</div>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
			<div
				v-for="advisory in advisories"
				:key="advisory.name"
				class="flex flex-col justify-between rounded-lg border p-5"
			>
				<div>
					<div class="mb-3 flex items-center justify-between">
						<span class="font-mono text-sm text-ink-gray-5">
							{{ advisory.name }}
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
