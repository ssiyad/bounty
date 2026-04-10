import type { BreadcrumbsProps } from "frappe-ui";
import { ref } from "vue";

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
