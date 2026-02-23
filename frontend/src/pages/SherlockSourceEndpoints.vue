<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Badge, createDocumentResource, createListResource, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Unused Functions"),
}));

const route = useRoute();
const sourceId = route.params.source as string;
const guestAccess = ref(false);

const endpoints = createListResource({
	doctype: "Sherlock Python Function",
	fields: ["*"],
	filters: {
		whitelisted: 1,
		source: sourceId,
	},
	pageLength: 99999,
	auto: true,
});

const source = createDocumentResource({
	doctype: "Bounty Target",
	name: sourceId,
	auto: true,
});

watch(guestAccess, (b) => {
	endpoints.filters.guest_access = b ? 1 : undefined;
	endpoints.reload();
});

const githubLink = (endpoint: any) => {
	return `${source.doc.repository}/blob/develop/${endpoint.path}#L${endpoint.line_number}`;
};
</script>

<template>
	<div class="overflow-y-auto">
		<div class="w-full divide-y leading-relaxed">
			<div class="flex divide-x font-medium">
				<div class="w-12 px-4 py-2"></div>
				<div class="w-96 px-4 py-2">Path</div>
				<div class="grow px-4 py-2">Name</div>
				<div class="w-20 px-4 py-2 text-end">Line</div>
				<div class="w-56 px-4 py-2 text-end">Arguments</div>
			</div>
			<div
				class="flex divide-x truncate"
				v-for="(endpoint, index) in endpoints.data"
				:key="endpoint.name"
			>
				<div class="w-12 px-4 py-2 flex items-center justify-center">
					{{ index + 1 }}
				</div>
				<div class="w-96 px-4 py-2 truncate">{{ endpoint.path }}</div>
				<div class="grow px-4 py-2 font-medium">
					<div class="flex items-center justify-between">
						<a :href="githubLink(endpoint)" target="_blank">
							{{ endpoint.function_name }}
						</a>
						<div class="flex items-center gap-2">
							<Badge
								v-if="endpoint.guest_access"
								theme="orange"
								variant="outline"
								label="Guest"
							/>
							<a
								:href="
									source.doc.repository + '/commit/' + endpoint.last_seen_commit
								"
								target="_blank"
							>
								<Badge v-if="endpoint.last_seen_commit">
									{{ endpoint.last_seen_commit.slice(0, 7) }}
								</Badge>
							</a>
							<Badge v-if="endpoint.last_author">
								{{ endpoint.last_author }}
							</Badge>
						</div>
					</div>
				</div>
				<div class="w-20 px-4 py-2 text-end">{{ endpoint.line_number }}</div>
				<div class="w-56 px-4 py-2 text-end text-wrap">{{ endpoint.arguments }}</div>
			</div>
		</div>
	</div>
</template>
