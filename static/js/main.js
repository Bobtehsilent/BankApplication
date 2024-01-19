{	
	class Details {
		constructor() {
			this.DOM = {};

			const detailsTmpl = `
			<div class="details__bg details__bg--down">
				<button class="details__close"><i class="fas fa-2x fa-times icon--cross tm-fa-close"></i></button>
				<div class="details__description"></div>
			</div>						
			`;

			this.DOM.details = document.createElement('div');
			this.DOM.details.className = 'details';
			this.DOM.details.innerHTML = detailsTmpl;
			// DOM.content.appendChild(this.DOM.details);
			document.getElementById('tm-wrap').appendChild(this.DOM.details);
			this.init();
		}
		init() {
			this.DOM.bgDown = this.DOM.details.querySelector('.details__bg--down');
			this.DOM.description = this.DOM.details.querySelector('.details__description');
			this.DOM.close = this.DOM.details.querySelector('.details__close');

			this.initEvents();
		}
		initEvents() {
			// close page when outside of page is clicked.
			document.body.addEventListener('click', () => this.close());
			// prevent close page when inside of page is clicked.
			this.DOM.bgDown.addEventListener('click', function(event) {
							event.stopPropagation();
						});
			// close page when cross button is clicked.
			this.DOM.close.addEventListener('click', () => this.close());
		}
		fill(info) {
			// fill current page info
			this.DOM.description.innerHTML = info.description;
		}		
		getProductDetailsRect(){
			var p = 0;
			var d = 0;

			try {
				p = this.DOM.productBg.getBoundingClientRect();
				d = this.DOM.bgDown.getBoundingClientRect();	
			}
			catch(e){}

			return {
				productBgRect: p,
				detailsBgRect: d
			};
		}
		open(data) {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.style.display = 'block';  

			this.DOM.details.classList.add('details--open');
			if (data && data.productBg) {
				this.DOM.productBg = data.productBg;
				this.DOM.productBg.style.opacity = 0;
			}
			const rect = this.getProductDetailsRect();

			this.DOM.bgDown.style.transform = `translateX(${rect.productBgRect.left-rect.detailsBgRect.left}px) translateY(${rect.productBgRect.top-rect.detailsBgRect.top}px) scaleX(${rect.productBgRect.width/rect.detailsBgRect.width}) scaleY(${rect.productBgRect.height/rect.detailsBgRect.height})`;
            this.DOM.bgDown.style.opacity = 1;

            // animate background
            anime({
                targets: [this.DOM.bgDown],
                duration: (target, index) => index ? 800 : 250,
                easing: (target, index) => index ? 'easeOutElastic' : 'easeOutSine',
                elasticity: 250,
                translateX: 0,
                translateY: 0,
                scaleX: 1,
                scaleY: 1,                              
                complete: () => this.isAnimating = false
            });

            // animate content
            anime({
                targets: [this.DOM.description],
                duration: 1000,
                easing: 'easeOutExpo',                
                translateY: ['100%',0],
                opacity: 1
            });

            // animate close button
            anime({
                targets: this.DOM.close,
                duration: 250,
                easing: 'easeOutSine',
                translateY: ['100%',0],
                opacity: 1
            });

            this.setCarousel();

            window.addEventListener("resize", this.setCarousel);
		}
		close() {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.classList.remove('details--open');

			anime({
                targets: this.DOM.close,
                duration: 250,
                easing: 'easeOutSine',
                translateY: '100%',
                opacity: 0
            });

            anime({
                targets: [this.DOM.description],
                duration: 20,
                easing: 'linear',
                opacity: 0
            });

            const rect = this.getProductDetailsRect();
            anime({
                targets: [this.DOM.bgDown],
                duration: 250,
                easing: 'easeOutSine',                
                translateX: (target, index) => {
                    return index ? rect.productImgRect.left-rect.detailsImgRect.left : rect.productBgRect.left-rect.detailsBgRect.left;
                },
                translateY: (target, index) => {
                    return index ? rect.productImgRect.top-rect.detailsImgRect.top : rect.productBgRect.top-rect.detailsBgRect.top;
                },
                scaleX: (target, index) => {
                    return index ? rect.productImgRect.width/rect.detailsImgRect.width : rect.productBgRect.width/rect.detailsBgRect.width;
                },
                scaleY: (target, index) => {
                    return index ? rect.productImgRect.height/rect.detailsImgRect.height : rect.productBgRect.height/rect.detailsBgRect.height;
                },
                complete: () => {
                    this.DOM.bgDown.style.opacity = 0;
                    this.DOM.bgDown.style.transform = 'none';
					if (this.DOM.productBg) {
                    	this.DOM.productBg.style.opacity = 1;
					}
                    this.DOM.details.style.display = 'none';                    
                    this.isAnimating = false;
                }
            });
		}
		// Slick Carousel
        setCarousel() {
          
	        var slider = $('.details .tm-img-slider');

	        if(slider.length) { // check if slider exist

		        if (slider.hasClass('slick-initialized')) {
		            slider.slick('destroy');
		        }

		        if($(window).width() > 767){
		            // Slick carousel
		            slider.slick({
		                dots: true,
		                infinite: true,
		                slidesToShow: 4,
		                slidesToScroll: 3
		            });
		        }
		        else {
		            slider.slick({
			            dots: true,
			            infinite: true,
			            slidesToShow: 2,
			            slidesToScroll: 1
		        	});
		     	}	
	        }          
        }
		fillCountryData(countryData) {
			let content = `<h2>Customers in ${countryData.countryName}</h2><ul>`;
			countryData.customers.forEach(customer => {
				content += `<li>${customer.name} - ${customer.email}</li>`;
			});
			content += `</ul>`;
			this.DOM.description.innerHTML = content;
		}
		fillCustomerData(customerData) {
			console.log(customerData); // Check what data is received
			let content = `<h2>${customerData.GivenName} ${customerData.Surname}</h2>`;
			content += `<p>Email: ${customerData.EmailAddress}</p>`;
			content += `<p>Country: ${customerData.Country}</p>`;
			// Add other fields as needed
			this.DOM.description.innerHTML = content;
			this.DOM.details.classList.add('table-details-box');
		}
	}; // class Details

	class Item {
		constructor(el) {
			this.DOM = {};
			this.DOM.el = el;
			this.DOM.product = this.DOM.el.querySelector('.product');
			this.DOM.productBg = this.DOM.product.querySelector('.product__bg');

			this.info = {
				description: this.DOM.product.querySelector('.product__description').innerHTML
			};

			this.initEvents();
		}
		initEvents() {
			this.DOM.product.addEventListener('click', () => this.open());
		}
		open() {
			if (this.DOM.el.classList.contains('map-container')) {
				// Handle map container differently or do nothing
			} else {
				if (this.DOM.productBg) {
					DOM.details.fill(this.info);
					DOM.details.open({
						productBg: this.DOM.productBg
					});
				}
			}
		}		
	}; // class Item
	class CustomerItem {
		constructor(el) {
			this.DOM = { el: el };
			try {
				console.log(this.DOM.el.getAttribute('data-customer'));
				this.customerData = JSON.parse(this.DOM.el.getAttribute('data-customer'));
			} catch (e) {
				console.error('Error parsing JSON:', e);
				// Handle the error or set a default value
				this.customerData = {};
			}
			this.i
			this.initEvents();
		}
		initEvents() {
			this.DOM.el.addEventListener('click', () => {
				DOM.details.fillCustomerData(this.customerData);
				DOM.details.open();
			});
			this.DOM.el.addEventListener('click', () => {
				document.querySelectorAll('.table-row').forEach(row => row.classList.remove('active'));
				this.DOM.el.classList.add('active');
			});
		}
	}; //Customer item class

	class AdminItem {
		constructor(el) {
			this.DOM = { el: el};
			this.DOM.product = this.DOM.el.querySelector('.product');
			this.DOM.productBg = this.DOM.product.querySelector('.product__bg');

			this.info = {
				description: this.DOM.product.querySelector('.product__description').innerHTML
			};

			this.initEvents();
		}
		initEvents() {
			this.DOM.product.addEventListener('click', () => this.open());
		}
		open() {
			if (this.DOM.productBg) {
				DOM.details.fill(this.info);
				DOM.details.open({
					productBg: this.DOM.productBg
				});
			}
		}
	}

	const DOM = {};

	DOM.grid = document.querySelector('.grid');
	if (DOM.grid) {
		DOM.content = DOM.grid.parentNode;
		DOM.gridItems = Array.from(DOM.grid.querySelectorAll('.grid__item')).filter(item => item.querySelector('.product'));
		let items = [];
		DOM.gridItems.forEach(item => items.push(new Item(item)));
		DOM.details = new Details();
	}

	DOM.adminItems = document.querySelectorAll('.admin-stat-item');
    if (DOM.adminItems.length) {
        let adminItems = [];
        DOM.adminItems.forEach(item => adminItems.push(new AdminItem(item)));
        DOM.details = new Details();
    }

	if (document.querySelector('.table-list')) {
		DOM.customerRows = document.querySelectorAll('.table-row');
		DOM.customerRows.forEach(row => new CustomerItem(row));
		DOM.details = new Details();
	}

	window.DOM = DOM;
	

	function openDetailsWithData(data) {
		console.log("Data received:", data); // Debugging line 
		//if (!data.productBg) {
		//	data.productBg = someDefaultElement;
		//}
		DOM.details.fillCountryData(data);
		DOM.details.open(data);
	}
};

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function clearSearch() {
	document.querySelector('input[name="search"]').value = '';
	document.querySelector('form').submit();
}

document.getElementById('sidebarToggle').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar-wrapper');
    sidebar.classList.toggle('collapsed');
});

// $(window).resize(function() {
//     var map = $('#europe-map').vectorMap('get', 'mapObject');
//     map.updateSize();
// });


window.openDetailsWithData = openDetailsWithData;
