<script setup lang="ts">
import { computed, ref } from "vue";
import { Dialog, Sidebar } from "frappe-ui";
import UserIcon from "~icons/lucide/user";
import AppearanceIcon from "~icons/lucide/eye";
import BankingIcon from "~icons/lucide/credit-card";
import SettingsProfile from "./SettingsProfile.vue";
import Upcoming from "../Upcoming.vue";

withDefaults(
	defineProps<{
		modelValue: boolean;
	}>(),
	{
		modelValue: false,
	},
);

defineEmits<{
	(e: "update:modelValue", value: boolean): void;
}>();

const active = ref("profile");

const activeComponent = computed(() => {
	switch (active.value) {
		case "profile":
			return SettingsProfile;
		case "appearance":
			return Upcoming;
		case "banking":
			return Upcoming;
		default:
			return Upcoming;
	}
});
</script>

<template>
	<Dialog
		:model-value="modelValue"
		@update:model-value="$emit('update:modelValue', $event)"
		:options="{
			size: '4xl',
		}"
	>
		<template #body>
			<div class="h-[600px] flex">
				<Sidebar
					disable-collapse
					:sections="[
						{
							label: 'Settings',
							items: [
								{
									label: 'Profile',
									icon: UserIcon,
									isActive: active === 'profile',
									onClick: () => (active = 'profile'),
								},
								{
									label: 'Appearance',
									icon: AppearanceIcon,
									isActive: active === 'appearance',
									onClick: () => (active = 'appearance'),
								},
								{
									label: 'Banking',
									icon: BankingIcon,
									isActive: active === 'banking',
									onClick: () => (active = 'banking'),
								},
							],
						},
					]"
				/>
				<div class="grow">
					<component :is="activeComponent" />
				</div>
			</div>
		</template>
	</Dialog>
</template>
