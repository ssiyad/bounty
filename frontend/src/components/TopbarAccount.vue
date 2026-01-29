<script setup lang="ts">
import { Button, Dropdown } from "frappe-ui";
import router from "@/router";
import { session } from "../data/session";

const options = [
	{
		label: "Logout",
		icon: "log-out",
		onClick: () => session.logout.submit(),
	},
];
</script>

<template>
	<Dropdown :options="options" placement="right">
		<Button
			label="Account"
			icon-left="user"
			@click.stop.prevent="
				(event: PointerEvent) => {
					if (!session.isLoggedIn) {
						event.stopPropagation();
						event.preventDefault();
						router.replace('/login');
					}
				}
			"
		/>
	</Dropdown>
</template>
