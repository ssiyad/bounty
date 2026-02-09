<script setup lang="ts">
import { ref, watch } from "vue";
import {
	Avatar,
	Button,
	Select,
	createDocumentResource,
	createListResource,
	usePageMeta,
} from "frappe-ui";
import LucideCodeXml from "~icons/lucide/code-xml";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Unused Functions"),
}));

const sourceName = ref("");

const endpoints = createListResource({
	doctype: "Sherlock Python Function",
	fields: ["*"],
	filters: {
		whitelisted: 1,
		source: sourceName,
	},
	pageLength: 99999,
});

const sources = createListResource({
	doctype: "Bounty Target",
	auto: true,
	fields: ["*"],
	pageLength: 99999,
});

const source = createDocumentResource({
	doctype: "Bounty Target",
	name: sourceName,
	auto: false,
});

watch(sourceName, () => {
	source.reload();
	endpoints.fetch();
});

const openCommit = (commit: string) => {
	if (commit) {
		const url = source.doc.repository + "/commit/" + commit;
		window.open(url, "_blank");
	}
};

const githubLink = (endpoint: any) => {
	return `${source.doc.repository}/blob/develop/${endpoint.path}#L${endpoint.line_number}`;
};
</script>

<template>
	<div class="px-4 py-3 border-b">
		<Select
			:options="
				sources.data?.map((source) => ({
					label: source.name,
					value: source.name,
					logo: source.logo,
				}))
			"
			v-model="sourceName"
			class="w-max"
			placeholder="Source"
		>
			<template #prefix>
				<LucideCodeXml class="size-4" />
			</template>
			<template #option="{ option }">
				<div class="flex items-center gap-2">
					<img
						v-if="option.logo"
						class="flex size-4 items-center justify-center rounded-[5px]"
						:src="option.logo"
						:alt="option.logo"
					/>
					<Avatar v-else :label="option.label" shape="square" size="xs" />
					<span>{{ option.label }}</span>
				</div>
			</template>
		</Select>
	</div>
	<div class="overflow-y-auto">
		<div class="w-full divide-y leading-relaxed">
			<div class="flex divide-x font-medium">
				<div class="w-12 px-4 py-3"></div>
				<div class="w-56 px-4 py-3">Path</div>
				<div class="grow px-4 py-3">Name</div>
				<div class="w-20 px-4 py-3 text-end">Line</div>
				<div class="w-56 px-4 py-3 text-end">Arguments</div>
			</div>
			<div
				class="flex divide-x truncate"
				v-for="(endpoint, index) in endpoints.data"
				:key="endpoint.name"
			>
				<div class="w-12 px-4 py-3 flex items-center justify-center">
					{{ index + 1 }}
				</div>
				<div class="w-56 px-4 py-3 truncate">{{ endpoint.path }}</div>
				<div class="grow px-4 py-3 font-medium">
					<div class="flex items-center justify-between">
						<a :href="githubLink(endpoint)" target="_blank">
							{{ endpoint.function_name }}
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
				<div class="w-56 px-4 py-3 text-end text-wrap">{{ endpoint.arguments }}</div>
			</div>
		</div>
	</div>
</template>
