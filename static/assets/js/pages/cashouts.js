"use strict";
var KTDatatablesAdvancedFooterCalllback = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');

		// begin first table
		table.DataTable({
			responsive: true,
			pageLength: 10,
			lengthMenu: [[5, 10, 25, 100, -1], [5, 10, 25, 100, 'All']],
			footerCallback: function(row, data, start, end, display) {

				var column = 5;
				var api = this.api(), data;

				// Remove the formatting to get integer data for summation
				var intVal = function(i) {
					return typeof i === 'string' ? i.replace(/[\$,]/g, '') * 1 : typeof i === 'number' ? i : 0;
				};

				// Total over all pages
				var total = api.column(column).data().reduce(function(a, b) {
					return intVal(a) + intVal(b);
				}, 0);

				// Total over this page
				var pageTotal = api.column(column, {page: 'current'}).data().reduce(function(a, b) {
					return intVal(a) + intVal(b);
				}, 0);

				// Update footer
				$(api.column(column).footer()).html(
					KTUtil.numberString(pageTotal.toFixed(0)) + '<br/> ( ' + KTUtil.numberString(total.toFixed(0)) + ' total )',
				);
			},
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