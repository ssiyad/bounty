<script setup lang="ts">
import { Dialog, Sidebar } from "frappe-ui";
import UserIcon from "~icons/lucide/user";
import AppearanceIcon from "~icons/lucide/eye";
import BankingIcon from "~icons/lucide/credit-card";
import SettingsProfile from "./SettingsProfile.vue";
</script>

<template>
	<Dialog
		:model-value="true"
		:options="{
			size: '4xl',
		}"
	>
		<template #body>
			<div class="h-[512px] flex">
				<Sidebar
					disable-collapse
					:sections="[
						{
							label: 'Settings',
							items: [
								{
									label: 'Profile',
									icon: UserIcon,
									onClick: () => {},
								},
								{
									label: 'Appearance',
									icon: AppearanceIcon,
									onClick: () => {},
								},
								{
									label: 'Banking',
									icon: BankingIcon,
									onClick: () => {},
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
