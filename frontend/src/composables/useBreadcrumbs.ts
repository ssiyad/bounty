import { ref } from "vue";
import type { BreadcrumbsProps } from "frappe-ui";

type BreadcrumbItem = BreadcrumbsProps["items"][number];

const breadcrumbs = ref<BreadcrumbItem[]>([]);

export const useBreadcrumbs = () => {
	const set = (items: BreadcrumbItem[]) => {
		breadcrumbs.value = items;
	};

	const reset = () => {
		breadcrumbs.value = [];
	};

	return { breadcrumbs, set, reset };
};
