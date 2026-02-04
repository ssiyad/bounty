<template>
	<div class="overflow-y-auto">
		<pre>
		{{ JSON.stringify(lens, null, 2) }}
	</pre
		>
	</div>
</template>

<script setup lang="ts">
import { Button, createResource, Textarea, TextInput, usePageMeta } from "frappe-ui";
import { hunterResource, hunterSaveResource } from "../data/hunter";
import { session } from "../data/session";
import { pageTitle } from "../utils/page";

usePageMeta(() => ({
	title: pageTitle("Sherlock"),
}));

const lens = createResource({
	url: "bounty.sherlock.lens.modules",
	auto: true,
});
</script>
