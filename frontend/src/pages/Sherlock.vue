<script setup lang="ts">
import { createListResource, usePageMeta } from "frappe-ui";
import Target from "../components/Target.vue";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Sherlock"),
}));

const sources = createListResource({
	doctype: "Bounty Target",
	auto: true,
	fields: ["*"],
	pageLength: 99999,
});
</script>

<template>
	<div class="overflow-y-auto">
		<div class="w-full divide-y leading-relaxed">
			<div class="flex divide-x font-medium">
				<div class="w-12 px-4 py-2"></div>
				<div class="w-56 px-4 py-2">Source</div>
				<div class="grow px-4 py-2 text-end">Repository</div>
			</div>
			<div
				class="flex divide-x truncate"
				v-for="(source, index) in sources.data"
				:key="source.name"
			>
				<div class="w-12 px-4 py-2 flex items-center justify-center">
					{{ index + 1 }}
				</div>
				<div class="w-56 px-4 py-2">
					<RouterLink
						:to="{
							name: 'SherlockSource',
							params: {
								source: source.name,
							},
						}"
					>
						<Target :target="source.name" />
					</RouterLink>
				</div>
				<div class="grow px-4 py-2 text-end">
					<a :href="source.repository" target="_blank">
						{{ source.repository }}
					</a>
				</div>
			</div>
		</div>
	</div>
</template>
