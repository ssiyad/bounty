<script setup lang="ts">
import { computed, ref, watch, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	Button,
	TextEditor,
	TextEditorFixedMenu,
	createDocumentResource,
	createResource,
} from "frappe-ui";
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

const buttons = [
	"Paragraph",
	["Heading 2", "Heading 3", "Heading 4"],
	"Separator",
	"Bold",
	"Italic",
	"Separator",
	"Bullet List",
	"Numbered List",
	"Separator",
	"Link",
	"Image",
];

const draft = createDocumentResource({
	doctype: "Bounty Draft",
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
				doctype: "Bounty Draft",
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
	<div class="size-full container">
		<div class="grow px-5 py-8">
			<div class="mb-4 pb-6 border-b">
				<input
					class="bg-transparent text-3xl border-none p-0 font-semibold focus:ring-0"
					placeholder="Title"
					:value="title"
					@input="title = $event.target.value"
				/>
			</div>
			<TextEditor
				editor-class="prose-sm max-w-none leading-relaxed"
				placeholder="Describe the problem..."
				:content="content"
				@change="content = $event"
			>
				<template #top>
					<div class="mb-4 flex flex-col justify-between">
						<TextEditorFixedMenu class="-ml-1 overflow-x-auto" :buttons="buttons" />
					</div>
				</template>
			</TextEditor>
		</div>
	</div>
</template>
