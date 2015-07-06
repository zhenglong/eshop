angular.module('App', ['utility','base'])
	.controller('MainCtrl', ['enums', 'ajax', '_', '$scope', 'base', function(enums, ajax, _, $scope, base) {
		$scope.base = base;
		var actions = {
			save: '/api/commodity-meta/',
			batchDelete: '/api/commodity-meta/batch-delete/',
			delete: '/api/commodity-meta/delete/',
			query: '/api/commodity-metas/',
			get: '/api/commodity-meta/',
			fetchCategories: '/api/categories/'
		};
		var currentQuery = {
			keyword: null,
			category_id: null
		};
		$scope.query = angular.copy(currentQuery);
		$scope.isQueryEmpty = function() {
			return !currentQuery.keyword && !currentQuery.category_id;
		};
		$scope.categories = [];
		
		$scope.fieldTypes = enums.getDataSource(enums.fieldType);
		
		$scope.metas = [];
		
		var defaultVm = {
			id:null,
			name: null,
			category_id: null,
			fields: []
		};
		$scope.vm = angular.copy(defaultVm);
		
		$scope.getCategoryName = function(categoryId) {
			return (_.find($scope.categories, function(c) {
				return c.id == categoryId;
			}) || {}).name;
		};
		
		$scope.isAddingMeta = function() {
			return !$scope.vm.id;
		};
		
		$scope.checkAll = false;
		
		$scope.checkAllChanged = function() {
			angular.forEach($scope.metas, function(meta) {
				meta.isSelected = $scope.checkAll;
			});
		};
		
		$scope.onAddField = function() {
			$scope.vm.fields.push({
				field_name: null,
				field_type: null,
				note: null
			});
		};
		
		$scope.onRemoveField = function(field) {
			$scope.vm.fields.splice($scope.vm.fields.indexOf(field), 1);
		};
		
		function _delete(ids) {
			ajax.delete(actions.batchDelete, ids)
				.success(function(result) {
					for(var i = 0; i < $scope.metas.length;) {
						if (ids.indexOf($scope.metas[i].id) > -1) {
							$scope.metas.splice(i, 1);
						} else {
							i++;
						}
					}
				});
		}
		
		$scope.onBatchDeleteMetas = function() {
			var ids = _.map(_.filter($scope.metas, function(meta) {
					return meta.isSelected;
				}), function(meta) {
					return meta.id;
				});
			_delete(ids);
		};
		
		$scope.onDeleteMeta = function(meta) {
			_delete([meta.id]);
		};
		$scope.onPreUpdateMeta = function(meta) {
			ajax.get(actions.get + meta.id, {})
				.success(function(result) {
					$scope.vm = result.data;
					$('#addCommodityMetaModal').foundation('reveal', 'open');				
				});
		};
		$scope.onPreAddMeta = function() {
			angular.copy(defaultVm, $scope.vm);
		};
		
		$scope.onClearQuery = function() {
			$scope.query.keyword = null;
			$scope.query.category_id = null;
			angular.copy($scope.query, currentQuery);
			$scope.onSearch();
		};
		
		$scope.onPreEditQuery = function() {
			currentQuery = angular.copy($scope.query);
		};
		
		$scope.onCancelToEditQuery = function() {
			if (currentQuery) angular.copy(currentQuery, $scope.query);
			$('#filterCommodityMetaModal').foundation('reveal', 'close');
		};
		
		$scope.onSearch = function() {
			ajax.get(actions.query, $scope.query).success(function(result) {
				currentQuery = angular.copy($scope.query);
				angular.forEach(result.data, function(d) {
					d.isSelected = false;
				});
				$scope.metas = result.data;
				$('#filterCommodityMetaModal').foundation('reveal', 'close');
			});
		};
		
		$scope.onSave = function($e) {
			ajax.save(actions.save, $scope.vm)
				.success(function(result) {
					if (!$scope.vm.id) {
						$scope.vm.id = result.id;
						$scope.metas.splice(0, 0, $scope.vm);
					} else {
						var meta = _.find($scope.metas, function(m) {
							return m.id == $scope.vm.id;
						});
						angular.copy($scope.vm, meta);
					}
					$('#addCommodityMetaModal').foundation('reveal', 'close');
				});
		};
		
		$scope.onCancel = function() {
			$('#addCommodityMetaModal').foundation('reveal', 'close');
		};
		
		(function onInitialize() {
			$scope.base.onInitialize();
			ajax.get(actions.fetchCategories, { listFlat : true })
				.success(function(result) {
					$scope.categories = result.data;
				}).then($scope.onSearch);
		})();
	}]);
