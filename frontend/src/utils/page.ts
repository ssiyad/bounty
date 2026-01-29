export const pageTitle = (title?: string) => {
  if (!title) {
    return "Frappe Bounty";
  }
  return title + " " + " - Frappe Bounty";
};
