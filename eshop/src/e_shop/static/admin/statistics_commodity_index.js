require.config({
	baseUrl:'/static/bower_components/',
	paths:{
		echarts:'echarts/build/dist'
	}
});
require(['echarts', 'echarts/chart/pie', 'echarts/chart/funnel'], function(ec) {
	angular.module('App', ['utility','base'])
	.controller('MainCtrl', ['$scope', 'ajax', 'base', function($scope, ajax, base) {
		$scope.base = base;
		(function onInitialize() {
			$scope.base.onInitialize();
			var myChart = ec.init(document.getElementById('chart-container'));
			myChart.setOption(option = {
				tooltip : {
					trigger: 'item',
					formatter: "{a} <br/>{b} : {c} ({d}%)"
				},
				legend: {
					orient : 'vertical',
					x : 'left',
					data:['宝贝#1','宝贝#2','宝贝#3','宝贝#4','宝贝#5','宝贝#6','宝贝#7','其它']
				},
				toolbox: {
					show : true,
					feature : {
						mark : {show: true},
						dataView : {show: true, readOnly: false},
						magicType : {
							show: true, 
							type: ['pie', 'funnel'],
							option: {
								funnel: {
									x: '25%',
									width: '50%',
									funnelAlign: 'left',
									max: 1548
								}
							}
						},
						restore : {show: true},
						saveAsImage : {show: true}
					}
				},
				calculable : true,
				series : [
					{
						name:'单品销售额',
						type:'pie',
						radius : '55%',
						center: ['50%', '60%'],
						data:[
							{value:1548, name:'宝贝#5'},
							{value:335, name:'宝贝#1'},
							{value:310, name:'宝贝#2'},
							{value:234, name:'宝贝#3'},
							{value:234, name:'宝贝#6'},
							{value:135, name:'宝贝#4'},
							{value:135, name:'宝贝#7'},
							{value:100, name:'其它'},
						]
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

