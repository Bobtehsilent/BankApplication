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
			let p = 0;
			let d = 0;

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
                duration: 250,
                easing: 'easeOutExpo',                
                // translateY: ['100%',0],
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
                duration: 100,
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
                duration: 100,
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
          
	        let slider = $('.details .tm-img-slider');

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
			let content =  `<div class="customer-details-container">`

			//column 1
			content += `<div class="customer-info">
							<h2>${customerData.GivenName} ${customerData.Surname}</h2>
							<p>Birthday:\n ${customerData.Birthday}</p>
							<p>Personal Number:\n ${customerData.PersonalNumber}</p>
							<p>Address: ${customerData.Streetaddress}</p>
							<p>Zipcode:\n ${customerData.Zipcode}, City: ${customerData.City}</p>
							<p>Country:\n ${customerData.Country}</p>
							<p>Phone Number:\n ${customerData.Telephone}</p>
							<p>Email:\n ${customerData.EmailAddress}</p>
						</div>`;

			content += `<div class="customer-accounts">
						<h3>Accounts</h3>`;
			if (customerData.Accounts) {
				let i = 1;
				customerData.Accounts.forEach(account => {
					content += `<p>${account.AccountType} ${i}: ${account.Balance}</p>`;
					i++
				});
			} else {
				content += `<div class="customer-accounts">
								<p>No accounts found</p>`;
			}
			content += `<p class="total-balance">Total Balance: ${customerData.total_balance}</p>
						</div>`;

				content += `<div class="customer-transactions">
                    <canvas id="balanceGraph"></canvas>
                    <div>
                        <!-- Buttons to toggle account types in the graph -->
                        <button onclick="toggleAccountType('savings')">Savings</button>
                        <button onclick="toggleAccountType('checking')">Checking</button>
                        <!-- Add more buttons as needed -->
                    </div>
                </div>`;

    		content += `</div>`; // Closing the container div

			// Add other fields as needed
			this.DOM.description.innerHTML = content;
			this.DOM.details.classList.add('table-details-box');

			fetch(`/graph_transactions/${customerData.Id}`)
				.then(response => response.json())
				.then(transactionData => {
					renderGraph(transactionData);
			});
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

//function for clear button on searches
function clearSearch() {
	document.querySelector('input[name="search"]').value = '';
	document.querySelector('form').submit();
}

// function managing closing and opening the side dashboards

document.addEventListener("DOMContentLoaded", function() {
    const sidebarWrapper = document.getElementById('sidebar-wrapper');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const pageContentWrapper = document.getElementById('page-content-wrapper');

    // Function to set sidebar state
    function setSidebarState(collapsed) {
        if (collapsed) {
            sidebarWrapper.classList.add('collapsed');
            pageContentWrapper.classList.remove('expanded'); // Remove expanded class when collapsed
        } else {
            sidebarWrapper.classList.remove('collapsed');
            pageContentWrapper.classList.add('expanded'); // Add expanded class when not collapsed
        }
        localStorage.setItem('sidebarCollapsed', collapsed);
    }

    // Function to toggle sidebar state
    function toggleSidebar() {
        const isCollapsed = sidebarWrapper.classList.contains('collapsed');
        setSidebarState(!isCollapsed);
    }

    // Set initial state of sidebar from localStorage
    const sidebarShouldBeCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    setSidebarState(sidebarShouldBeCollapsed);

    // Toggle sidebar on button click
    sidebarToggle.addEventListener('click', toggleSidebar);
});


function openGraph(customerId) {
    // Fetch data
    fetch(`/graph_transactions/${customerId}?account_types=savings&account_types=checking`)
        .then(response => response.json())
        .then(data => {
            // Process data and render graph
            renderGraph(data);
        });
}

function renderGraph(data) {
    // Example data processing (modify according to your data structure)
    const labels = data.map(item => item.date); // Array of dates
    const dataPoints = data.map(item => item.balance); // Array of balances

    const ctx = document.getElementById('balanceGraph').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Account Balance',
                data: dataPoints,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Show the graph container
    document.getElementById('graph-container').style.display = 'block';
}

function toggleAccountType(accountType) {
    // Get all transaction elements
    const transactionElements = document.querySelectorAll('.transaction');

    // Loop through each transaction element
    transactionElements.forEach(transactionEl => {
        // Check if the transaction belongs to the specified account type
        if (transactionEl.dataset.accountType === accountType) {
            // Toggle visibility
            if (transactionEl.style.display === 'none') {
                transactionEl.style.display = '';
            } else {
                transactionEl.style.display = 'none';
            }
        }
    });
}

document.getElementById('navToggle').addEventListener('click', function() {
    var linksContainer = document.querySelector('.tm-nav-table-container');
    var mainContent = document.querySelector('.tm-main-content');
    linksContainer.classList.toggle('active');

    if (linksContainer.classList.contains('active')) {
        mainContent.style.marginTop = (linksContainer.offsetHeight + 60) + 'px';
    } else {
        mainContent.style.marginTop = '60px';
    }
});


// $(window).resize(function() {
//     let map = $('#europe-map').vectorMap('get', 'mapObject');
//     map.updateSize();
// });


window.openDetailsWithData = openDetailsWithData;
