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

export const hunterSaveResource = createResource({
  url: "frappe.client.save",
  method: "POST",
  auto: false,
  makeParams: (data: any) => ({
    doc: data,
  }),
  onSuccess: (data: any) => {
    hunterResource.setData(data);
  },
});
