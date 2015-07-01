angular.module('base', ['utility'])
	.factory('base', ['ajax', '$window', function(ajax, $window) {
		return {
			logout: function() {
				ajax.post('/account/logout/',{})
					.success(function() {
						$window.location.href = '/manage/categories';
					});
			}
		};
	}]);
