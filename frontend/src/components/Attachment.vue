<script setup lang="ts">
import { Button, Dialog } from "frappe-ui";
import { ref } from "vue";

defineProps<{
	name: string;
	url: string;
}>();

const open = ref(false);
const iframeRef = ref<HTMLIFrameElement | null>(null);

function setFrameSize() {
	const iframe = iframeRef.value;
	if (iframe && iframe.contentWindow && iframe.contentDocument) {
		const body = iframe.contentDocument.body;
		iframe.style.height = body.scrollHeight + "px";
		iframe.style.width = body.scrollWidth + "px";
	}
}
</script>

<template>
	<div class="text-sm text-ink-gray-8 cursor-pointer hover:text-ink-gray-9" @click="open = true">
		{{ name }}
	</div>
	<Dialog v-model="open" :options="{ size: '4xl' }">
		<template #body>
			<div class="h-12 px-5 flex items-center justify-between gap-2">
				<div class="font-medium">{{ name }}</div>
				<div class="space-x-2">
					<a :href="url" target="_blank" rel="noopener noreferrer">
						<Button label="Open Externally" @click="open = false" />
					</a>
					<Button label="Close" @click="open = false" />
				</div>
			</div>
			<iframe ref="iframeRef" class="w-full" :src="url" @load="setFrameSize()" />
		</template>
	</Dialog>
</template>
