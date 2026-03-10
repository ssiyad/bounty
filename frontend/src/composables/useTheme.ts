import { ref } from "vue";

export type Theme = "light" | "dark" | "system";

const current = ref<Theme>("system");

const resolveAndApply = (theme: Theme) => {
	if (theme === "system") {
		const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
		document.documentElement.setAttribute("data-theme", prefersDark ? "dark" : "light");
	} else {
		document.documentElement.setAttribute("data-theme", theme);
	}
};

export const useTheme = () => {
	const setTheme = (theme: Theme) => {
		current.value = theme;
		localStorage.setItem("theme", theme);
		resolveAndApply(theme);
	};

	const initTheme = () => {
		const saved = localStorage.getItem("theme") as Theme | null;
		const theme = saved ?? "system";
		current.value = theme;
		resolveAndApply(theme);
	};

	return { current, setTheme, initTheme };
};
