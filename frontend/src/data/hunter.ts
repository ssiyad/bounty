import { createResource } from "frappe-ui";
import { session } from "./session";

export const hunterResource = createResource({
  url: "frappe.client.get",
  cache: "Hunter",
  auto: !!session.user,
  makeParams: () => ({
    doctype: "Bounty Hunter",
    filters: {
      user_id: session.user,
    },
  }),
});
