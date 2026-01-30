<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Avatar, Badge, createDocumentResource, usePageMeta } from "frappe-ui";
import { statusTheme, categoryTheme, severityTheme } from "../utils/badgeThemes";
import { pageTitle } from "../utils/page";

const route = useRoute();
const attemptId = route.params.id as string;

const attemptResource = createDocumentResource({
	doctype: "Bounty Attempt",
	name: attemptId,
	auto: !!attemptId,
});

const attempt = computed(() => attemptResource.doc);

const targetResource = createDocumentResource({
	doctype: "Bounty Target",
	name: attempt.value?.target,
	cache: ["Bounty Target", attempt.value?.target],
	auto: !!attempt.value?.target,
});

const target = computed(() => targetResource.doc);

usePageMeta(() => ({
	title: pageTitle(attempt.value?.title),
}));
</script>

<template>
	<div class="container mx-auto py-16">
		<div v-if="attempt" class="grid grid-cols-3">
			<div class="col-span-2 pr-4">
				<div class="text-3xl font-medium mb-4">
					{{ attempt.title }}
				</div>
				<p class="leading-relaxed">
					{{ attempt.content }}
				</p>
			</div>
			<div class="col-span-1 border-l pl-4 py-4 space-y-4">
				<div v-if="target" class="flex items-center justify-between">
					<p class="text-sm">Target</p>
					<a :href="target.repository" target="_blank">
						<div class="flex items-center gap-2">
							<img
								v-if="target.logo"
								class="flex size-6 items-center justify-center rounded-[5px]"
								:src="target.logo"
								:alt="target.name"
							/>
							<Avatar v-else :label="target.name" shape="square" />
							<div class="font-medium">
								{{ attempt.target }}
							</div>
						</div>
					</a>
				</div>
				<hr />
				<div class="flex items-center justify-between">
					<p class="text-sm">Status</p>
					<div>
						<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Category</p>
					<div>
						<Badge
							:label="attempt.category"
							:theme="categoryTheme(attempt.category)"
						/>
					</div>
				</div>
				<div class="flex items-center justify-between">
					<p class="text-sm">Severity</p>
					<div>
						<Badge
							:label="attempt.severity"
							:theme="severityTheme(attempt.severity)"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
