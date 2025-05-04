		let moment = require("moment-timezone");
		let hours = moment.tz('Asia/Manila').format('HHmm');
		let session = (
		hours > 0001 && hours <= 400 ? "Blessed Morning" : 
		hours > 401 && hours <= 700 ? "Morning" :
		hours > 701 && hours <= 1000 ? "Morning" :
		hours > 1001 && hours <= 1100 ? "Morning" : 
		hours > 1100 && hours <= 1500 ? "Afternoon" : 
		hours > 1501 && hours <= 1800 ? "Evening " : 
		hours > 1801 && hours <= 2100 ? "Evening.." : 
		hours > 2101 && hours <= 2400 ? "Late Night Sleep Well..." : 
		"error");