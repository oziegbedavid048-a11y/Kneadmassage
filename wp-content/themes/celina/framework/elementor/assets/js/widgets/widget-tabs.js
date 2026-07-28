(
	function( $ ) {
		'use strict';

		var celinaTabsHandler = function( $scope, $ ) {
			var $tabs = $scope.find( '.celina-tabs' );

			var $tabTitle = $tabs.children( '.celina-tabs-wrapper' ).children( '.celina-tab-title' );
			var $tabMobileTitle = $tabs.children( '.celina-tabs-content-wrapper' ).children( '.celina-tab-title' );
			var $tabContent = $tabs.children( '.celina-tabs-content-wrapper' ).children( '.celina-tab-content' );

			// Active first tab.
			showTab( 1 );

			$tabs.on( 'click', '.celina-tab-title', function( e ) {
				e.preventDefault();
				e.stopPropagation();

				var activeTab = $( this ).data( 'tab' );

				showTab( activeTab );
			} );

			function showTab( tabIndex ) {
				$tabContent.each( function() {
					var currentTab = $( this ).data( 'tab' );
					if ( tabIndex === currentTab ) {
						$( this ).show();
						$( this ).addClass( 'celina-active' );
					} else {
						$( this ).hide();
						$( this ).removeClass( 'celina-active' );
					}
				} );

				$tabTitle.each( function() {
					var currentTab = $( this ).data( 'tab' );

					if ( tabIndex === currentTab ) {
						$( this ).addClass( 'celina-active' );
					} else {
						$( this ).removeClass( 'celina-active' );
					}
				} );

				$tabMobileTitle.each( function() {
					var currentTab = $( this ).data( 'tab' );

					if ( tabIndex === currentTab ) {
						$( this ).addClass( 'celina-active' );
					} else {
						$( this ).removeClass( 'celina-active' );
					}
				} );
			}
		};

		$( window ).on( 'elementor/frontend/init', function() {
			elementorFrontend.hooks.addAction( 'frontend/element_ready/yolo_tabs.default', celinaTabsHandler );
		} );
	}
)( jQuery );
