angular.module('App', ['utility','base'])
	.controller('MainCtrl', ['_', 'utility', 'ajax', '$scope', 'base','history', function(_, utility, ajax, $scope, base, history) {
		$scope.base = base;
		var actions = {
			save: '/api/user-profile/',
			fileUpload: '/api/user-profile/upload-photo/',
		};
		var imageSize = '?height=137&width=137';
		var defaultUserImage = '/static/images/unknown.svg';
		$scope.photo = {
			data:''
		};
		$scope.vm = {
			name:null,
			address:null,
			moble:null,
			tel:null
		};
		$scope.onStartUpload = function() {
			$('#file-upload').click();
		};
		$scope.onSave = function() {
			var param = {
				id: $scope.vm.id,
				name: $scope.vm.name,
				company_name: $scope.vm.company_name
			};
			param.photo = $scope.photo.id;
			ajax.save(actions.save, param).success(function(result) {
				history.back();
			});
		};
		(function onInitialize() {
			
			$('#file-upload').fileupload({
				url:actions.fileUpload,
				headers: {
					'X-CSRFTOKEN':$('[name="csrfmiddlewaretoken"]').val(),
					'Authorization':'Bearer '+window.access_token
				},
				done: function(e, data) {
					var file = angular.fromJson(data.result.data);
					file.thumbnail = file.thumbnail + imageSize;
					ajax.get(file.thumbnail)
						.success(function(result) {
							file.data = result; // base-64 image data
							$scope.base.userPhoto = result;
							angular.copy(file, $scope.photo);
						});
				}
			});
			ajax.get(actions.save, {})
				.success(function(result) {
					var data = result.data;
					if (data.photos) {
						var photo = data.photos[0];
						photo.thumbnail += imageSize;
						ajax.get(photo.thumbnail)
							.success(function(result) {
								photo.data = result;
								$scope.base.userPhoto = result;
								angular.copy(photo, $scope.photo);
							});
					} else {
						$scope.photo.data = defaultUserImage;
					}
					if (data.photos) delete data.photos;
					angular.copy(data, $scope.vm);
				});
		})();
	}]);

