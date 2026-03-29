export const statusTheme = (status: string) => {
	switch (status) {
		case "Accepted":
			return "green";
		case "Rejected":
			return "red";
		case "Pending":
			return "orange";
		default:
			return "gray";
	}
};

export const categoryTheme = (status: string) => {
	switch (status) {
		case "Bug":
			return "blue";
		case "Security":
			return "red";
		default:
			return "gray";
	}
};

export const severityTheme = (status: string) => {
	switch (status) {
		case "Informational":
			return "gray";
		case "Low":
			return "green";
		case "Medium":
			return "blue";
		case "High":
			return "orange";
		case "Critical":
			return "red";
		default:
			return "gray";
	}
};
