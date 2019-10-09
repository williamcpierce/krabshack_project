"use strict";
var KTDatatablesAdvancedFooterCalllback = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');

		// begin first table
		table.DataTable({
			responsive: true,
			pageLength: 10,
			lengthMenu: [[5, 10, 25, 100, -1], [5, 10, 25, 100, 'All']],
		});
	};

	return {

		//main function to initiate the module
		init: function() {
			initTable1();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesAdvancedFooterCalllback.init();
});