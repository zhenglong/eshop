angular.module('App', ['utility', 'ngSanitize', 'ngCkeditor','base'])
	.controller('MainCtrl', ['_', 'utility', 'ajax', 'history', '$sce', '$window', '$scope', 'base', function(_, utility, ajax, history, $sce, $window, $scope, base) {
		$scope.base = base;
		var actions = {
			save: '/api/commodity/',
			get: '/api/commodity/',
			getMeta: '/api/commodity-meta/',
			fetchCategories: '/api/categories/',
			queryMetas: '/api/commodity-metas/',
			fileUpload: '/api/commodity/add-file/',
			deleteFile: '/api/commodity/delete-file/'
		};
		var imageSize = '?height=200&width=200';
		var ignoreMetaChange = false;
		$scope.editorOptions = {
			extraPlugins:'autogrow,confighelper,image2',
			autoGrow_onStartup:true,
			filebrowserImageUploadUrl: '/api/file/upload-from-ckeditor/'
		};
		$scope.categories = [];
		$scope.metas = [];
		$scope.vm = {
			id: $window.commodity_id,
			name: null,
			brand_id: null,
			category_id: null,
			meta_id: null,
			base_price: null,
			discount_price: null,
			stock: null,
			description: null,
			left_fields: [],
			right_fields: []
		};
		$scope.isMetaChange = false;
		function _onCategoryChanged() {
			return ajax.get(actions.queryMetas, {category_id:$scope.vm.category_id})
				.success(function(result) {
					$scope.metas = result.data;
					$scope.vm.meta_id = null;
				});
		}
		$scope.onCategoryChanged = function() {
			_onCategoryChanged();
		};
		function _onMetaChange() {
			$scope.isMetaChange = true;
			$scope.vm.left_fields.splice(0, $scope.vm.left_fields.length);
			$scope.vm.right_fields.splice(0, $scope.vm.right_fields.length);
		}
		$scope.$watch('vm.meta_id', function(newV, oldV) {
			if (newV != oldV && !ignoreMetaChange) _onMetaChange();
			ignoreMetaChange && (ignoreMetaChange = false);
		});
		$scope.onMetaChanged = function() {
			//_onMetaChange();
		};
		$scope.onGenerateDetails = function() {
			ajax.get(actions.getMeta + $scope.vm.meta_id, {})
				.success(function(result) {
					var meta = result.data;
					meta.fields = _.map(meta.fields, function(f) {
						return {
							custom_field_id: f.id,
							field_name: f.field_name,
							field_type: f.field_type,
							value: null
						};
					});
					for(var i = 0; i< meta.fields.length; i+=2) {
						$scope.vm.left_fields.push(meta.fields[i]);
						if ((i+1) < meta.fields.length) $scope.vm.right_fields.push(meta.fields[i+1]);
					}
					$scope.isMetaChange = false;
				});
		};
		$scope.onSave = function() {
			var param = {
			id: $scope.vm.id,
			name: $scope.vm.name,
			brand_id: $scope.vm.brand_id,
			category_id: $scope.vm.category_id,
			meta_id: $scope.vm.meta_id,
			base_price: $scope.vm.base_price,
			discount_price: $scope.vm.discount_price,
			stock: $scope.vm.stock,
			description: $scope.vm.description,
			details:[],
			photos:[]
			};
			var len = Math.min($scope.vm.left_fields.length, $scope.vm.right_fields.length),
				left = $scope.vm.left_fields, right = $scope.vm.right_fields,
				longer = (len == left.length) ? right : left;
			for(var i = 0; i < len; i++) {
				param.details.push({
					custom_field_id: left[i].custom_field_id,
					value:left[i].value
				});
				param.details.push({
					custom_field_id: right[i].custom_field_id,
					value:right[i].value
				});
			}
			while(i < longer.length) {
				param.details.push({
					custom_field_id: longer[i].custom_field_id,
					value:longer[i].value
				});
				i++;
			}
			if (!param.id) {
				param.photos = _.map($scope.files, function(f) {
					return f.id;
				});
			}
			ajax.post(actions.save, param)
				.success(function(result) {
					history.back();
				});
		};
		$scope.onCancel = function() {
		};
		$scope.onDeleteFile = function(file) {
			ajax.delete(actions.deleteFile + utility.queryParams({object_id : $scope.vm.id}), 
				{file_id:file.id})
				.success(function(result) {
					$scope.files.splice($scope.files.indexOf(file),1);
				});
		};
		$scope.files = [];
		(function onInitialize() {
			$('#file-upload').fileupload({
				url:actions.fileUpload + utility.queryParams({object_id : $scope.vm.id}),
				done: function(e, data) {
					var file = angular.fromJson(data.result.data);
					file.thumbnail = file.thumbnail + imageSize;
					$scope.files.push(file);
					$scope.$apply();
				}
			});
			ajax.get(actions.fetchCategories, { listFlat : true })
				.success(function(result) {
					$scope.categories = result.data;
				}).then(function() {
					if ($scope.vm.id) {
						$scope.$on('ckeditor.ready', function() {
							ajax.get(actions.get+$scope.vm.id, {})
								.success(function(result) {
									var data = result.data;
									$scope.vm.id = data.id;
									$scope.vm.name = data.name;
									$scope.vm.brand_id = data.brand_id;
									$scope.vm.category_id = data.category_id;
									_onCategoryChanged().success(function() {
										ignoreMetaChange = true;
										var oldMetaId = $scope.vm.meta_id;
										$scope.vm.meta_id = data.meta_id;
										ignoreMetaChange = (oldMetaId != data.meta_id);
										for(var i = 0; i< data.details.length; i+=2) {
											$scope.vm.left_fields.push(data.details[i]);
											if ((i+1) < data.details.length) $scope.vm.right_fields.push(data.details[i+1]);
										}
									});
									$scope.vm.base_price = data.base_price;
									$scope.vm.discount_price = data.discount_price;
									$scope.vm.stock = data.stock;
									$scope.vm.description = data.description;
									angular.forEach(data.photos, function(p) {
										p.thumbnail += imageSize;
									});
									$scope.files = $scope.files.concat(data.photos);
								});
						});
					}
				});
		})();
	}]);

