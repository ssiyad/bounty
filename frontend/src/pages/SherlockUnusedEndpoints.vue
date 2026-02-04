<template>
	<div class="overflow-y-auto">
		<div class="w-full divide-y leading-relaxed">
			<div class="flex divide-x font-medium">
				<div class="w-12 px-4 py-3"></div>
				<div class="w-56 px-4 py-3">Parent</div>
				<div class="grow px-4 py-3">Name</div>
				<div class="w-20 px-4 py-3 text-end">Line</div>
				<div class="w-56 px-4 py-3 text-end">Args</div>
			</div>
			<div
				class="flex divide-x truncate"
				v-for="(endpoint, index) in unusedEndpoints.data"
				:key="endpoint.id"
			>
				<div class="w-12 px-4 py-3 flex items-center justify-center">{{ index + 1 }}</div>
				<div class="w-56 px-4 py-3 truncate">{{ endpoint.parent }}</div>
				<a
					:href="githubLink(endpoint)"
					target="_blank"
					class="block grow px-4 py-3 font-medium"
				>
					{{ endpoint.name }}
				</a>
				<div class="w-20 px-4 py-3 text-end">{{ endpoint.line_number }}</div>
				<div class="w-56 px-4 py-3 text-end text-wrap">
					{{ endpoint.args.join(", ") }}
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { createResource, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Unused Functions"),
}));

const unusedEndpoints = createResource({
	url: "bounty.sherlock.lens.unused_endpoints",
	auto: true,
});

const githubLink = (endpoint: any) => {
	return `https://github.com/frappe/press/blob/develop/${endpoint.path}#L${endpoint.line_number}`;
};
</script>
