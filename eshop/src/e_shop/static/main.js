$(function() {
	$('.my-tabs .my-tab-item').click(function() {
		var $this = $(this);
		$('.my-tabs .my-tab-item.active').removeClass('active');
		$('.my-tabs .my-tab-page.active').removeClass('active');
		$this.addClass('active');
		$($this.attr('href')).addClass('active');
	});
});
