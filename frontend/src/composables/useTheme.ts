import { onUnmounted, ref } from "vue";

export type Theme = "light" | "dark" | "system";

const current = ref<Theme>("system");

let mediaQuery: MediaQueryList | null = null;

const resolveAndApply = (theme: Theme) => {
	if (theme === "system") {
		const prefersDark =
			mediaQuery?.matches ??
			window.matchMedia("(prefers-color-scheme: dark)").matches;
		document.documentElement.setAttribute(
			"data-theme",
			prefersDark ? "dark" : "light",
		);
	} else {
		document.documentElement.setAttribute("data-theme", theme);
	}
};

const handleSystemThemeChange = () => {
	if (current.value === "system") {
		resolveAndApply("system");
	}
};

export const useTheme = () => {
	const setTheme = (theme: Theme) => {
		current.value = theme;
		localStorage.setItem("theme", theme);
		resolveAndApply(theme);
	};

	const initTheme = () => {
		mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
		mediaQuery.addEventListener("change", handleSystemThemeChange);

		const saved = localStorage.getItem("theme") as Theme | null;
		const theme = saved ?? "system";
		current.value = theme;
		resolveAndApply(theme);
	};

	onUnmounted(() => {
		mediaQuery?.removeEventListener("change", handleSystemThemeChange);
	});

	return { current, setTheme, initTheme };
};
