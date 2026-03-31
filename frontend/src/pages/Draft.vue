<script setup lang="ts">
import { computed, ref, watch, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	Button,
	TextEditor,
	createDocumentResource,
	createResource,
} from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import Attachments from "@/components/Attachments.vue";
import SeveritySelector from "@/components/selects/SeveritySelector.vue";
import TargetSelector from "@/components/selects/TargetSelector.vue";

const route = useRoute();
const router = useRouter();
const id = route.query.id as string;

const draft = createDocumentResource({
	doctype: "FS Draft",
	name: id || "draft",
	auto: !!id,
	whitelistedMethods: {
		submit: {
			method: "submit_draft",
			onSuccess: () => router.replace({ name: "Reports" }),
		},
	},
});

if (!draft.doc) {
	draft.setDoc({
		doctype: "FS Draft",
		title: "",
		content: "",
		target: "",
		severity: "",
	});
}

const save = () => {
	// if (!draft.isDirty) return;
	if (!draft.doc.title) return;
	if (draft.doc.name) return draft.save.submit();
	createResource({
		url: "frappe.client.insert",
		auto: true,
		makeParams: () => ({
			doc: {
				doctype: "FS Draft",
				title: draft.doc.title,
				content: draft.doc.content,
				target: draft.doc.target,
				severity: draft.doc.severity,
			},
		}),
		onSuccess: (draft_: any) => {
			router.replace({
				name: "Draft",
				query: {
					id: draft_.name,
				},
			});
			draft.name = draft_.name;
			draft.setDoc(draft_);
		},
	});
};

const { set } = useBreadcrumbs();

watchEffect(() => {
	set([
		{
			label: "Drafts",
			route: { name: "Drafts" },
		},
		{
			label: draft.doc?.title || "New",
		},
	]);
});
</script>

<template>
	<Teleport defer to="#topbar-actions">
		<Button
			v-if="draft.doc?.name"
			label="Submit"
			icon-right="arrow-right"
			variant="solid"
			@click="draft.submit.submit()"
		/>
	</Teleport>
	<div class="flex grow overflow-hidden divide-x">
		<div class="grow overflow-y-auto">
			<div v-if="!id || draft.doc" class="py-14 max-w-[840px] mx-auto">
				<div class="mb-4 pb-6 border-b">
					<input
						class="bg-transparent text-3xl border-none p-0 font-semibold focus:ring-0 w-full"
						placeholder="Title"
						:value="draft.doc.title"
						@input="draft.doc.title = $event.target.value"
						@blur="save()"
					/>
				</div>
				<TextEditor
					bubble-menu
					editor-class="prose-sm max-w-none leading-relaxed"
					placeholder="Type '/' for commands"
					:content="draft.doc.content"
					:upload-args="{
						doctype: draft.doc?.doctype,
						docname: draft.doc?.name,
						private: true,
						optimize: true,
					}"
					@change="draft.doc.content = $event"
					@blur="save()"
				/>
			</div>
		</div>
		<div class="w-72 shrink-0 px-5 py-4 space-y-3">
			<div v-if="!id || draft.doc" class="flex items-center justify-between">
				<div class="text-sm font-medium">Target</div>
				<TargetSelector v-model="draft.doc.target" @update:model-value="save()" />
			</div>
			<div v-if="!id || draft.doc" class="flex items-center justify-between">
				<div class="text-sm font-medium">Severity</div>
				<SeveritySelector v-model="draft.doc.severity" @update:model-value="save()" />
			</div>
			<Attachments
				v-if="draft.doc?.name"
				class="border-t pt-3"
				doctype="FS Draft"
				:docname="draft.doc.name"
			/>
		</div>
	</div>
</template>
