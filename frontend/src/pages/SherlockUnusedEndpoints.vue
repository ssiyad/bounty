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
				<div class="grow px-4 py-3 font-medium">
					<div class="flex items-center justify-between">
						<a :href="githubLink(endpoint)" target="_blank">
							{{ endpoint.name }}
						</a>
						<div
							class="flex items-center gap-2"
							v-if="endpoint.last_user || endpoint.last_commit"
						>
							<Button
								icon="git-branch"
								variant="ghost"
								v-if="endpoint.last_commit"
								@click="openCommit(endpoint.last_commit)"
							/>
							{{ endpoint.last_user }}
						</div>
					</div>
				</div>
				<div class="w-20 px-4 py-3 text-end">{{ endpoint.line_number }}</div>
				<div class="w-56 px-4 py-3 text-end text-wrap">
					{{ endpoint.args.join(", ") }}
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { Button, createDocumentResource, createResource, usePageMeta } from "frappe-ui";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Unused Functions"),
}));

const unusedEndpoints = createResource({
	url: "bounty.sherlock.lens.unused_endpoints",
	auto: true,
	makeParams: () => ({
		target: "Cloud",
	}),
});

const target = createDocumentResource({
	doctype: "Bounty Target",
	name: "Cloud",
	auto: true,
});

const openCommit = (commit: string) => {
	if (commit) {
		const url = target.doc.repository + "/commit/" + commit;
		window.open(url, "_blank");
	}
};

const githubLink = (endpoint: any) => {
	return `${target.doc.repository}/blob/develop/${endpoint.path}#L${endpoint.line_number}`;
};
</script>
