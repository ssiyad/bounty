<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Badge, createDocumentResource, usePageMeta } from "frappe-ui";
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

usePageMeta(() => ({
	title: pageTitle(attempt.value.title),
}));
</script>

<template>
	<div class="container mx-auto py-16">
		<div class="grid grid-cols-3">
			<div class="col-span-2 pr-4">
				<div class="text-3xl font-medium mb-4">
					{{ attempt.title }}
				</div>
				<p class="leading-relaxed">
					{{ attempt.content }}
				</p>
			</div>
			<div class="col-span-1 border-l pl-4 py-4 space-y-4">
				<div class="flex items-center justify-between">
					<div>Status</div>
					<div>
						<Badge :label="attempt.status" :theme="statusTheme(attempt.status)" />
					</div>
				</div>
				<div class="flex items-center justify-between">
					<div>Category</div>
					<div>
						<Badge
							:label="attempt.category"
							:theme="categoryTheme(attempt.category)"
						/>
					</div>
				</div>
				<div class="flex items-center justify-between">
					<div>Severity</div>
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
