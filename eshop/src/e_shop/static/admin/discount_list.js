angular.module('App', ['utility','base'])
	.controller('MainCtrl', ['$scope', 'moment', 'ajax', 'base', function($scope, moment, ajax, base) {
		$scope.base = base;
		var actions = {
			listEvents: '/api/discounts/',
			fetchEvent: '', // not used until now
			publicEvent: '/api/discount/'
		};
		var dateFormat = 'YYYY-MM-DD';
		$scope.currentEvent = {
			id:null,
			name:null,
			dateRange:null,
			limit_per_user:null,
			is_all_applied:true,
			discount:0.8,
			type:null
		};
		$scope.onPublish = function() {
		};
		$scope.onReset = function() {
			$scope.currentEvent.id = null;
			$scope.currentEvent.name = null;
			$scope.currentEvent.dateRange = null;
			$scope.currentEvent.limit_per_user = null;
			$scope.currentEvent.is_all_applied = true;
			$scope.currentEvent.discount = 0.8;
			$scope.currentEvent.type = null;
		};
		(function onInitialize() {
			$scope.base.onInitialize();
			var startDate = moment().add(-6, 'month').format(dateFormat),
				endDate = moment().add(6, 'month').format(dateFormat);
			ajax.get(actions.listEvents, {startDate: startDate,endDate: endDate})
				.success(function(result) {
					//[
						//{id:1, content:'元旦促销', start:'2015-01-01', end:'2015-01-03', title:'元旦促销'},
						//{id:2, content:'妇女节促销', start:'2015-03-08'},
						//{id:3, content:'儿童节促销', start:'2015-06-01'},
						//{id:4, content:'劳动节促销', start:'2015-05-01', end:'2015-05-03'}
					//]
					var container = document.getElementById('timeline');
					var items = new vis.DataSet(_.map(result.data, function(d) {
							return {
								id:d.id,
								title:d.name,
								content:d.note,
								start:moment(d.start_date).format(dateFormat),
								end: moment(d.end_date).format(dateFormat),
								type:'box'
							};
						}));
					var options = {
						min:startDate,
						max:endDate,
						locale:'zh-cn',
						zoomMin:604800000
					};
					
					var timeline = new vis.Timeline(container, items, options);
					timeline.on('select', function(properties) {
						var event = _.find(result.data, function(d) {
							return d.id == properties.items[0];
						});
						angular.copy(event, $scope.currentEvent);
						$scope.currentEvent.dateRange = moment(event.start_date).format(dateFormat) + ' - ' + moment(event.end_date).format(dateFormat);
						$scope.$apply();
					});
				});
		})();
	}]);
