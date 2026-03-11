<script setup lang="ts">
import { TabButtons } from "frappe-ui";
import SunIcon from "~icons/lucide/sun";
import MoonIcon from "~icons/lucide/moon";
import MonitorIcon from "~icons/lucide/monitor";
import { useTheme, type Theme } from "@/composables/useTheme";

const { current, setTheme } = useTheme();

const themeButtons = [
	{ label: "Light", value: "light", icon: SunIcon },
	{ label: "Dark", value: "dark", icon: MoonIcon },
	{ label: "System", value: "system", icon: MonitorIcon },
];
</script>

<template>
	<div class="h-full overflow-y-auto p-4">
		<div class="h-7 flex items-center justify-between mb-6">
			<p class="text-lg font-medium">Preferences</p>
		</div>
		<div class="space-y-2">
			<p class="font-medium">Theme</p>
			<TabButtons
				class="w-max"
				:buttons="themeButtons"
				v-model="current"
				@update:model-value="setTheme"
			/>
		</div>
	</div>
</template>
