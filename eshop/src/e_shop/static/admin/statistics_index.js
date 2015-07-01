require.config({
	baseUrl:'/static/bower_components/',
	paths:{
		echarts:'echarts/build/dist'
	}
});
require(['echarts', 'echarts/chart/bar', 'echarts/chart/line'], function(ec) {
	angular.module('App', ['utility','base'])
	.controller('MainCtrl', ['$scope', 'ajax', 'base', function($scope, ajax, base) {
		$scope.base = base;
		(function onInitialize() {
			var myChart = ec.init(document.getElementById('chart-container'));
			myChart.setOption({
				tooltip : {
					trigger: 'axis',
					axisPointer : {            // 坐标轴指示器，坐标轴触发有效
						type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
					}
				},
				legend: {
					data:['2014年', '2015年']
				},
				toolbox: {
					show : true,
					orient: 'vertical',
					x: 'right',
					y: 'center',
					feature : {
						mark : {show: true},
						dataView : {show: true, readOnly: false},
						magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
						restore : {show: true},
						saveAsImage : {show: true}
					}
				},
				calculable : true,
				xAxis : [
					{
						type : 'category',
						data : ['星期六','星期日','星期一','星期二','星期三','星期四','今天']
					}
				],
				yAxis : [
					{
						type : 'value'
					}
				],
				series : [
					{
						name:'2015年',
						type:'bar',
						data:[320, 332, 301, 334, 390, 330, 320, 320]
					},
					{
						name:'2014年',
						type:'bar',
						data:[300, 32, 300, 84, 490, 230, 300, 320]
					}
				]
			});
			$(window).resize(function() {
				myChart.resize();
			});
		})();
	}]);
	angular.bootstrap(document, ['App']);
	$(document).foundation();
});

