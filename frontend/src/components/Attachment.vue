<script setup lang="ts">
import { Button, Dialog } from "frappe-ui";
import { ref } from "vue";

const props = defineProps<{
	name: string;
	url: string;
	filetype: string;
}>();

const open = ref(false);
const imageFileTypes = ["jpg", "jpeg", "png", "gif", "bmp", "webp"];
const isImage = imageFileTypes.includes(props.filetype.toLowerCase());
</script>

<template>
	<div class="text-sm text-ink-gray-8 cursor-pointer hover:text-ink-gray-9">
		<div v-if="isImage" @click="open = true">{{ name }}</div>
		<div v-else>
			<a :href="url" target="_blank" rel="noopener noreferrer">{{ name }}</a>
		</div>
	</div>
	<Dialog v-if="isImage" v-model="open" :options="{ size: '7xl' }">
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
			<img :src="url" />
		</template>
	</Dialog>
</template>
