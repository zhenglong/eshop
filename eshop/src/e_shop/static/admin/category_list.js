angular.module('App', ['utility', 'ngJsTree', 'base'])
	.controller('MainCtrl', ['$scope', '$log', '$window', 'ajax', '_', 'base', function($scope, $log, $window, ajax, _, base) {
		$scope.base = base;
		var rootName = '所有分类';
		var _isDirty = false;
		var actions = {
			saveCategory: '/api/category/',
			listCategory: '/api/categories/'
		};
		$scope.treeConfig = {
			core: {
				themes:{
					variant:'large'
				},
				'check_callback':true
			}
		};
		$scope.treeData = [{
			text: rootName,
			state: {
				opened:true,
				selected:true
			},
			children: []
		}];
		$scope.currentCategory = null;
		$scope.treeInstance = null;
		$scope.currentSubCategories = [];
		$scope.onAddSubCategory = function() {
			_isDirty = true;
			var category = _getCategory();
			category.state.adding = true;
			$scope.currentSubCategories.push(category);
		};
		function _getCategory(obj) {
			var isObj = obj && angular.isObject(obj);
			return {
				text: isObj ? obj.text : obj, 
				id: isObj ? obj.id : '',
				categoryId: isObj ? obj.original.categoryId : '',
				state: {
					removing:false, 
					adding:false, 
					updating:false
				},
				nodeData: isObj ? obj : null
			};
		}
		function _getCategoryFromViewModel(vm) {
			return {
				text: vm.name, 
				id: '',
				categoryId: vm.id,
				state: {
					removing:false, 
					adding:false, 
					updating:false,
					opened:true
				},
				nodeData: null
			};
		}
		$scope.onSaveAllChanges = function() {
			var tree = $scope.treeInstance.jstree(true);
			var param = {
				id : $scope.currentCategory.original.categoryId,
				name : $scope.currentCategory.text,
				children : []
			};
			angular.forEach($scope.currentSubCategories, function(v) {
				if (!v.state.removing) {					
					param.children.push({
						id : v.categoryId,
						name : v.text
					});
				}
			});
			ajax.post(actions.saveCategory, param)
				.success(function(result) {
					if (result && result.data) {
						angular.forEach($scope.currentSubCategories, function(v, i, collection) {
							if (v.state.adding) {
								v.categoryId = result.data[i];
								collection[i] = _getCategory(tree.get_node(tree.create_node($scope.currentCategory, v, 'last', null, true)));
							} else if (v.state.removing) {
								tree.delete_node(v.id);
							} else if (v.state.updating) {
								v.state.updating = false;
								tree.rename_node(v.id, v.text);
							} else {
								// still the same
							}
						});
						var i = 0;
						while(i < $scope.currentSubCategories.length) {
							if ($scope.currentSubCategories[i].state.removing) $scope.currentSubCategories.splice(i, 1);
							else i++;
						}
						//_changeSelection(tree.get_selected(true)[0]);
						tree.open_node(tree.get_selected(true)[0]);
						_isDirty= false;
					}
				});
		};
		var _suppressChangeEvent = false;
		function _cb() {
			var tree = $scope.treeInstance.jstree(true);
			if ($scope.currentCategory) {
				if ($scope.currentSubCategories && $scope.currentSubCategories.length) 
					$scope.currentSubCategories.splice(0, $scope.currentSubCategories.length);
				var temp = $scope.currentCategory.children && $scope.currentCategory.children.length ? 
					_.map($scope.currentCategory.children, function(nodeId) {
						return _getCategory(tree.get_node(nodeId));
					}) : [];
				if (temp.length) $scope.currentSubCategories.push.apply($scope.currentSubCategories, temp);
				$scope.$apply();
			}
		}
		function _changeSelection(obj) {
			var tree = $scope.treeInstance.jstree(true);
			if (obj.action == 'ready') {
				$scope.currentCategory = tree.get_node(obj.selected[0]);
				onIntialize(function() {
					$scope.currentCategory = tree.get_node($scope.currentCategory.id);
					_cb();
				});
			} else if (obj.node && (obj.node != $scope.currentCategory)) {
				$scope.currentCategory = obj.node;
				_cb();
			}
		}
		$scope.onChangeSelection = function($e, obj) {
			if (_suppressChangeEvent) return;
			var tree = $scope.treeInstance.jstree(true);
			if (_isDirty) {
				if ($window.confirm('是否放弃修改？')) {
					_isDirty = false;
					_changeSelection(obj);
				} else {
					_suppressChangeEvent = true;
					tree.deselect_all();
					tree.select_node($scope.currentCategory);
					_suppressChangeEvent = false;
				}
			} else {
				_changeSelection(obj);
			}
		};
		$scope.removeSubCategory = function($e, c) {
			function _act() {
				_isDirty = true;
				if (c.categoryId) {
					c.state.updating = false;
					c.state.adding = false;
					c.state.removing = true;
				} else {
					var index = $scope.currentSubCategories.indexOf(c);
					$scope.currentSubCategories.splice(c, 1);
				}
			}
			if (c.children && c.children.length) {
				if ($window.confirm('该分类有子分类，确定要删除它及其所有子分类吗？')) {
					_act();
				}
			} else {
				_act();
			}
		};
		$scope.onSubCategoryChanged = function($e, c) {
			if (!_isDirty) _isDirty = true;
			if (!c.state.adding) {
				if (c.nodeData) c.nodeData.state.updating = true;
				c.state.updating = true;
			}
		};
		function convertToTreeData(categories) {
			return _.map(categories, function(c) {
				var result = _getCategoryFromViewModel(c);
				if (c.children && c.children.length) {
					result.children = convertToTreeData(c.children);
				}
				return result;
			});
		}
		function onIntialize(cb) {
			return ajax.get(actions.listCategory, {
				//load the root-level categories
				categoryId:null,
				includeChildren:true
			}).success(function(result) {
				var arr = convertToTreeData(result.data);
				$scope.treeInstance.jstree(true)._append_json_data($scope.currentCategory, arr, cb);
			});
		};
	}]);
