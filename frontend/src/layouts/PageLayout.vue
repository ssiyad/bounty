<template>
	<div class="size-full flex overflow-hidden">
		<Sidebar v-if="!isMobile" />
		<div class="flex flex-col overflow-hidden grow pb-12 md:pb-0">
			<Topbar v-if="breadcrumbs.length" :breadcrumbs="breadcrumbs" />
			<Banner
				message="This is a work in progress. You may encounter rough edges."
				variant="info"
			>
				<a href="https://github.com/ssiyad/security/issues" target="_blank" rel="noopener">
					<Button label="Report an Issue" variant="ghost" icon-right="external-link" />
				</a>
			</Banner>
			<RouterView />
		</div>
		<MobileNav v-if="isMobile" />
	</div>
</template>

<script setup lang="ts">
import Banner from "@/components/Banner.vue";
import MobileNav from "@/components/MobileNav.vue";
import Sidebar from "@/components/Sidebar.vue";
import Topbar from "@/components/Topbar.vue";
import { useBreadcrumbs } from "@/composables/useBreadcrumbs";
import { Button } from "frappe-ui";
import { onMounted, onUnmounted, ref } from "vue";

const { breadcrumbs } = useBreadcrumbs();

const isMobile = ref(window.innerWidth < 768);

const handleResize = () => {
	isMobile.value = window.innerWidth < 768;
};

onMounted(() => {
	window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
	window.removeEventListener("resize", handleResize);
});
</script>
