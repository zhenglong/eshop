angular.module('App', ['utility', 'ui.select', 'ngSanitize','base'])
	.controller('MainCtrl', ['ajax', '_', '$sce', '$scope', 'base', function(ajax, _, $sce, $scope, base) {
		$scope.base = base;
		var actions = {
			save: '/api/commodity/',
			batchDelete: '/api/commodity/batch-delete/',
			delete: '/api/commodity/delete/',
			query: '/api/commodities/',
			get: '/api/commodity/',
			shelve: '/api/commodity/shelve/',
			batchShelve: '/api/commodity/batch-shelve/',
			fetchCategories: '/api/categories/',
			fetchDiscounts: '/api/discounts/'
		};
		var currentQuery = {
			keyword: null,
			category_id: null,
			is_off_shelve: false
		};
		$scope.query = angular.copy(currentQuery);
		
		$scope.categories = [];
		$scope.commodities = [];
		$scope.appliedDiscounts = [];
		$scope.discounts = [];
		var currentCommodity = null;
		$scope.discountModalTitle = function() {
			return $sce.trustAsHtml('设置折扣<em style="font-size:0.8em;">'+ (currentCommodity && currentCommodity.name) + '</em>');
		};
		
		$scope.checkAll = false;
		$scope.onCheckAllChanged = function() {
			angular.forEach($scope.commodities, function(commodity) {
				commodity.isSelected = $scope.checkAll;
			});
		};
		
		$scope.onBatchDeleteCommodities = function() {
			var ids = _.map(_.filter($scope.commodities, function(commodity) {
					return commodity.isSelected;
				}), function(commodity) {
					return commodity.id;
				});
			ajax.post(actions.batchDelete, ids).success(function(result) {
					for(var i = 0; i < $scope.commodities.length;) {
						if (ids.indexOf($scope.commodities[i].id) > -1) {
							$scope.commodities.splice(i, 1);
						} else {
							i++;
						}
					}
				});
		};
		$scope.onClearQuery = function() {
			$scope.query.keyword = null;
			$scope.query.category_id = null;
			$scope.query.is_off_shelve = false;
			angular.copy($scope.query, currentQuery);
			$scope.onSearch();
		};
		$scope.getCategoryName = function(categoryId) {
			return (_.find($scope.categories, function(c) {
				return c.id == categoryId;
			}) || {}).name;
		};
		$scope.onPreEditQuery = function() {
			currentQuery = angular.copy($scope.query);
		};
		$scope.onShelve = function(commodity) {
			ajax.post(actions.shelve, {
				commodity_id: commodity.id, 
				is_off_shelve: !$scope.query.is_off_shelve}).success(function() {
					$scope.commodities.splice($scope.commodities.indexOf(commodity), 1);
				});
		};
		$scope.onBatchShelve = function(commodity) {
			var ids = _.map(_.filter($scope.commodities, function(commodity) {
					return commodity.isSelected;
				}), function(commodity) {
					return commodity.id;
				});
			ajax.post(actions.batchShelve, {
				commodity_ids: ids, 
				is_off_shelve: !$scope.query.is_off_shelve}).success(function() {
					for(var i = 0; i < $scope.commodities.length;) {
						if (ids.indexOf($scope.commodities[i].id) > -1) {
							$scope.commodities.splice(i, 1);
						} else {
							i++;
						}
					}
				});
		};
		$scope.onCancelToEditQuery = function() {
			if (currentQuery) angular.copy(currentQuery, $scope.query);
			$('#filterCommodityModal').foundation('reveal', 'close');
		};
		$scope.onSearch = function() {
			ajax.get(actions.query, $scope.query).success(function(result) {
				currentQuery = angular.copy($scope.query);
				angular.forEach(result.data, function(d) {
					d.isSelected = false;
				});
				$scope.commodities = result.data;
				$('#filterCommodityModal').foundation('reveal', 'close');
			});
		};
		$scope.onCancelBatchDiscount = function() {
			$('#batchDiscountModal').foundation('reveal', 'close');
		};
		$scope.onDiscount = function(commodity) {
			currentCommodity = commodity;
			function _cb() {
				ajax.get(actions.fetchDiscounts, {commodity_id:commodity.id})
					.success(function(result) {
						$scope.appliedDiscounts = result.data;
					});
			}
			if (!$scope.discounts.length) {
				ajax.get(actions.fetchDiscounts, {})
					.success(function(result) {
						$scope.discounts = result.data;
					}).then(_cb);
			} else {
				_cb();
			}
		};
		$scope.onBatchDiscount = function() {
			$scope.appliedDiscounts = [];
			if (!$scope.discounts.length) {
				ajax.get(actions.fetchDiscounts, {})
					.success(function(result) {
						$scope.discounts = result.data;
					});
			}
		};
		(function onInitialize() {
			ajax.get(actions.fetchCategories, { listFlat : true })
				.success(function(result) {
					$scope.categories = result.data;
				}).then($scope.onSearch);
		})();
	}]);

