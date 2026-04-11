<script setup lang="ts">
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { formatDistanceToNow } from "date-fns";
import { createListResource, createResource } from "frappe-ui";
import { useRouter } from "vue-router";

const router = useRouter();
useBreadcrumbs().set([{ label: "Inbox" }]);

const notifications = createListResource({
	doctype: "FS Notification",
	auto: true,
	fields: [
		"name",
		"creation",
		"is_read",
		"reference_doctype",
		"reference_docname",
		"content",
	],
	orderBy: "creation desc",
	onSuccess: () => {
		createResource({
			url: "security.api.inbox.mark_read",
			auto: true,
		});
	},
});

const transform = (content: string) => {
	let result = content;
	// Regex to test against.
	const r =
		/frappe-security:reference-doc:doctype=([a-zA-Z]+)&docname=([a-zA-Z\d]+)&text=([a-zA-Z]+)/gm;
	for (const m of content.matchAll(r)) {
		// Find match, doctype, docname and text inside the original string.
		const match = m.shift();
		const doctype = m.shift();
		const docname = m.shift();
		const text = m.shift();
		if (!(match && doctype && docname && text)) return result;
		// Find actual route from router.
		const route = router.resolve({ name: doctype, params: { id: docname } });
		// Construct intended `a` tag.
		const url = `<a href="${route.href}" rel=\"noopener noreferrer\">${text}</a>`;
		// Replace original string with intended `a` tag.
		result = result.replace(match, url);
	}
	// Return transformed content.
	return result;
};
</script>

<template>
	<div class="overflow-y-auto">
		<div class="mx-auto max-w-[840px] py-6 md:py-14 px-4 md:px-0 w-full">
			<h1 class="text-2xl md:text-3xl font-semibold mb-4 md:mb-6">Inbox</h1>
			<div class="divide-y">
				<div
					v-for="notification in notifications.data"
					class="py-3 flex items-center justify-between"
					:class="{
						'opacity-80': notification.is_read,
					}"
				>
					<div
						class="[&_a]:font-medium [&_a]:text-ink-blue-3"
						v-html="transform(notification.content)"
					/>
					<div class="text-ink-gray-7">
						{{ formatDistanceToNow(notification.creation) }} ago
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
