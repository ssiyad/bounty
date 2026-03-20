<script setup lang="ts">
import { computed, ref, watch, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Button, TextEditor, createDocumentResource, createResource } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";

const debounce = (fn: () => void, delay: number) => {
	let timeout: ReturnType<typeof setTimeout> | null = null;
	return () => {
		if (timeout) {
			clearTimeout(timeout);
		}
		timeout = setTimeout(() => {
			fn();
		}, delay);
	};
};

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;
const isNew = computed(() => id === "new-report");

const title = ref("");
const content = ref("");

const draft = createDocumentResource({
	doctype: "FS Draft",
	name: id,
	auto: !!id && !isNew.value,
	whitelistedMethods: {
		submit: {
			method: "submit_draft",
			onSuccess: () => {
				router.replace({
					name: "Reports",
				});
			},
		},
	},
	onSuccess: (draft: any) => {
		title.value = draft.title;
		content.value = draft.content;
	},
});

const unsaved = computed(() => !draft.doc);

const debouncedSave = debounce(() => {
	draft.doc.title = title.value;
	draft.doc.content = content.value;
	draft.save.submit();
}, 500);

const createDraft = () => {
	createResource({
		url: "frappe.client.insert",
		auto: true,
		makeParams: () => ({
			doc: {
				doctype: "FS Draft",
				title: title.value,
				content: content.value,
			},
		}),
		onSuccess: (draft_: any) => {
			router.replace({
				name: "Draft",
				params: {
					id: draft_.name,
				},
			});
			draft.name = draft_.name;
			draft.setDoc(draft_);
		},
	});
};

let hasLoadedDraft = false;

watch(
	[title, content],
	() => {
		if (unsaved.value) return;
		if (!hasLoadedDraft) {
			hasLoadedDraft = true;
			return;
		}
		debouncedSave();
	},
	{ deep: false },
);

const { set } = useBreadcrumbs();

watchEffect(() => {
	set([
		{
			label: "Drafts",
			route: { name: "Drafts" },
		},
		{
			label: title.value || "New",
		},
	]);
});
</script>

<template>
	<Teleport defer to="#topbar-actions">
		<Button v-if="unsaved" label="Save" variant="solid" @click="createDraft()" />
		<Button v-else label="Submit" variant="solid" @click="draft.submit.submit()" />
	</Teleport>
	<div class="grow overflow-y-auto">
		<div class="py-14 max-w-[840px] mx-auto">
			<div class="mb-4 pb-6 border-b">
				<input
					class="bg-transparent text-3xl border-none p-0 font-semibold focus:ring-0 w-full"
					placeholder="Title"
					:value="title"
					@input="title = $event.target.value"
				/>
			</div>
			<TextEditor
				editor-class="prose-sm max-w-none leading-relaxed"
				placeholder="Type '/' for commands"
				:content="content"
				@change="content = $event"
				bubble-menu
			/>
		</div>
	</div>
</template>
