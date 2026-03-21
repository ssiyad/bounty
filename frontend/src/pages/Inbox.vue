<script setup lang="ts">
import { useRouter } from "vue-router";
import { createListResource, createResource } from "frappe-ui";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { formatDistanceToNow } from "date-fns";

const router = useRouter();
useBreadcrumbs().set([{ label: "Inbox" }]);

const notifications = createListResource({
	doctype: "FS Notification",
	auto: true,
	fields: ["name", "creation", "is_read", "reference_doctype", "reference_docname", "content"],
	orderBy: "creation desc",
});

const transform = (content: string) => {
	// Regex to test against.
	const r =
		/frappe-security:reference-doc:doctype=([a-zA-Z]+)&docname=([a-zA-Z\d]+)&text=([a-zA-Z]+)/gm;
	for (const m of content.matchAll(r)) {
		// Find match, doctype, docname and text inside the original string.
		const match = m.shift();
		const doctype = m.shift();
		const docname = m.shift();
		const text = m.shift();
		if (!(match && doctype && docname && text)) return;
		// Find actual route from router.
		const route = router.resolve({ name: doctype, params: { id: docname } });
		// Construct intended `a` tag.
		const url = `<a href="${route.href}" rel=\"noopener noreferrer\">${text}</a>`;
		// Replace original string with intended `a` tag.
		content = content.replace(match, url);
	}
	// Return transformed content.
	return content;
};

createResource({
	url: "security.api.inbox.mark_read",
	auto: true,
});
</script>

<template>
	<div class="overflow-y-auto">
		<div class="mx-auto max-w-[840px] py-14 w-full">
			<h1 class="text-3xl font-semibold mb-6">Inbox</h1>
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
