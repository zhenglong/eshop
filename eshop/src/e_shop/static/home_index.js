angular.module('App', ['ionic', 'wu.masonry', 'slick'])
	.controller('MainCtrl', ['$scope', '$ionicSideMenuDelegate', function($scope, $ionicSideMenuDelegate) {
		$scope.toggleLeftSideMenu = function() {
			$ionicSideMenuDelegate.toggleLeft();
		};
		var bricks = [];
		for(var i = 0; i < 100; i++) {
			bricks.push({
				src: '/static/images/{0}.jpg'.format((i%10)+1)
			});
		}
		$scope.bricks = bricks;
	}]);
