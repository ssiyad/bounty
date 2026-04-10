<script setup lang="ts">
import AdvisoryCard from "@/components/AdvisoryCard.vue";
import SeveritySelector from "@/components/selects/SeveritySelector.vue";
import TargetSelector from "@/components/selects/TargetSelector.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { Button, createResource } from "frappe-ui";
import { type Ref, ref, watch } from "vue";

useBreadcrumbs().set([{ label: "Advisories" }]);

const target = ref("");
const severity = ref("");
const start = ref(0);
const limit = 10;

interface Advisory {
	name: string;
	title: string;
	frappe_reference: string;
	severity: string;
	target: string;
	published_on: string;
	reported_by?: string;
}

const a_: Ref<Advisory[]> = ref([]);
const count = ref(0);
const hasNextPage = ref(false);
const advisories = createResource({
	url: "security.api.advisory.get_advisories",
	auto: true,
	makeParams: () => ({
		start: start.value,
		limit: limit,
		target: target.value,
		severity: severity.value,
	}),
	onSuccess: ([data, count_, has_next_page]: [Advisory[], number, boolean]) => {
		a_.value.push(...data);
		count.value = count_;
		hasNextPage.value = has_next_page;
	},
});

const load = () => {
	start.value = start.value + 2;
	advisories.reload();
};

watch([target, severity], () => {
	a_.value = [];
	advisories.fetch();
});
</script>

<template>
	<div class="overflow-y-auto">
		<div class="mx-auto max-w-[840px] py-6 md:py-14 px-4 md:px-0 w-full">
			<h1 class="text-2xl md:text-3xl font-medium md:font-semibold mb-4 md:mb-6">Advisories</h1>
			<div class="mb-4 flex flex-col md:flex-row md:items-center gap-2">
				<TargetSelector v-model="target" class="w-full md:w-auto" />
				<SeveritySelector v-model="severity" class="w-full md:w-auto" />
			</div>
			<div class="flex flex-col gap-4">
				<AdvisoryCard
					v-for="advisory in a_"
					:key="advisory.name"
					:advisory="advisory"
				/>
			</div>
			<div v-if="hasNextPage" class="mt-4 text-center">
				<Button label="Load More" @click="load()" />
			</div>
		</div>
	</div>
</template>