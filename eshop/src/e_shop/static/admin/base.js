angular.module('base', ['utility'])
	.factory('base', ['ajax', '$window', function(ajax, $window) {
		return {
			userPhoto: null,
			logout: function() {
				ajax.post('/account/logout/',{})
					.success(function() {
						$window.location.href = '/manage/categories';
					});
			},
			onInitialize: function() {
				var _this = this;
				ajax.get('/api/user-profile/get-photo/', {})
					.success(function(result) {
						_this.userPhoto = result || '/static/images/unknown.svg';
					});
			}
		};
	}]);
