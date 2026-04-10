import router from "@/router";
import { createResource } from "frappe-ui";

export const userResource = createResource({
	url: "/api/method/frappe.auth.get_logged_user",
	cache: "User",
	auto: true,
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			router.push("/login");
		}
	},
});
