<script setup lang="ts">
import UpcomingPlaceholder from "@/components/UpcomingPlaceholder.vue";
import SettingsPreferences from "@/components/settings/SettingsPreferences.vue";
import SettingsProfile from "@/components/settings/SettingsProfile.vue";
import { Dialog, Sidebar } from "frappe-ui";
import { computed, ref } from "vue";
import PaymentIcon from "~icons/lucide/credit-card";
import AppearanceIcon from "~icons/lucide/eye";
import UserIcon from "~icons/lucide/user";

withDefaults(
	defineProps<{
		modelValue: boolean;
	}>(),
	{
		modelValue: false,
	},
);

defineEmits<(e: "update:modelValue", value: boolean) => void>();

const active = ref("profile");

const activeComponent = computed(() => {
	switch (active.value) {
		case "profile":
			return SettingsProfile;
		case "preferences":
			return SettingsPreferences;
		case "banking":
			return UpcomingPlaceholder;
		default:
			return UpcomingPlaceholder;
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
									label: 'Preferences',
									icon: AppearanceIcon,
									isActive: active === 'preferences',
									onClick: () => (active = 'preferences'),
								},
								{
									label: 'Payments',
									icon: PaymentIcon,
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