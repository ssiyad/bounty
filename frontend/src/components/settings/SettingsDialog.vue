<script setup lang="ts">
import { ref } from "vue";
import { Dialog, Sidebar } from "frappe-ui";
import UserIcon from "~icons/lucide/user";
import AppearanceIcon from "~icons/lucide/eye";
import BankingIcon from "~icons/lucide/credit-card";
import SettingsProfile from "./SettingsProfile.vue";

const active = ref("profile");
</script>

<template>
	<Dialog
		:model-value="true"
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
					<SettingsProfile />
				</div>
			</div>
		</template>
	</Dialog>
</template>
