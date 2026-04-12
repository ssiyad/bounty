import router from "@/router";
import { createResource } from "frappe-ui";
import { computed, reactive } from "vue";
import { userResource } from "./user";

const sessionUser = () => {
	const cookies = Object.fromEntries(
		document.cookie.split(";").map((c) => c.trim().split("=")),
	);
	let _sessionUser = cookies.user_id ?? null;
	if (_sessionUser === "Guest") {
		_sessionUser = null;
	}
	return _sessionUser;
};

export const session = reactive({
	login: createResource({
		url: "login",
		makeParams({ email, password }) {
			return { usr: email, pwd: password };
		},
		onSuccess() {
			userResource.reload();
			session.user = sessionUser();
			session.login.reset();
			router.replace("/");
		},
	}),

	logout: createResource({
		url: "logout",
		onSuccess() {
			userResource.reset();
			session.user = sessionUser();
			router.replace("/");
		},
	}),
	user: sessionUser(),
	isLoggedIn: computed(() => !!session.user),
});
