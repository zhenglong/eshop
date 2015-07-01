angular.module('App', ['utility','base'])
	.directive('ngEnter', function() {
		return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });
 
                event.preventDefault();
            }
        });
    };
	})
	.controller('MainCtrl', ['_', 'utility', 'ajax', '$scope', 'base', function(_, utility, ajax, $scope, base) {
		$scope.base = base;
		var actions = {
			save: '/api/brand/',
			listBrands: '/api/brands',
			deleteBrand: '/api/brand/delete/',
			fileUpload: '/api/brand/add-file/',
			deleteFile: '/api/brand/delete-file/'
		};
		var imageSize = '?height=137&width=137';
		$scope.brands = [];
		$scope.filtered = [];
		$scope.files = [];
		$scope.vm = {
			id:0,
			name:null,
			company_name:null
		};
		$scope.query = {
			name:null
		};
		$scope.onSearch = function() {
			$scope.filtered = _.filter($scope.brands, function(b) {
				return (b.name.indexOf($scope.query.name)>=0) || (b.company_name.indexOf($scope.query.name)>=0);
			});
		};
		$scope.onSave = function() {
			var param = {
				id: $scope.vm.id,
				name: $scope.vm.name,
				company_name: $scope.vm.company_name
			};
			param.photos = _.map($scope.files, function(f) {
				return f.id;
			});
			ajax.save(actions.save, param).success(function(result) {
				param.id = result.data;
				param.photos = $scope.files;
				$scope.files = [];
				$scope.vm.id = 0;
				$scope.vm.name = null;
				$scope.vm.company_name = null;
				$scope.brands.push(param);
				$('#addBrandModal').foundation('reveal', 'close');
			});
		};
		$scope.onCancel = function() {
				$scope.files = [];
				$scope.vm.id = 0;
				$scope.vm.name = null;
				$scope.vm.company_name = null;
				$('#addBrandModal').foundation('reveal', 'close');
		};
		$scope.onDeleteBrand = function(brand) {
			ajax.delete(actions.deleteBrand, brand.id).success(function() {
				$scope.brands.splice($scope.brands.indexOf(brand), 1);
			});
		};
		$scope.onDeleteFile = function(file) {
			ajax.delete(actions.deleteFile + utility.queryParams({object_id : $scope.vm.id}), 
				{file_id:file.id})
				.success(function(result) {
					$scope.files.splice($scope.files.indexOf(file),1);
				});
		};
		(function onInitialize() {
			$('#file-upload').fileupload({
				url:actions.fileUpload + utility.queryParams({object_id : 0}),
				done: function(e, data) {
					var file = angular.fromJson(data.result.data);
					file.thumbnail = file.thumbnail + imageSize;
					$scope.files.push(file);
					$scope.$apply();
				}
			});
			ajax.get(actions.listBrands, {})
				.success(function(result) {
					var data = result.data;
					angular.forEach(data, function(b) {						
						angular.forEach(b.photos, function(p) {
							p.thumbnail += imageSize;
						});
					});
					$scope.brands = data;
					$scope.filtered = $scope.brands;
				});
		})();
	}]);

