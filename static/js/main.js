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
			const appendTarget = document.getElementById('tm-wrap') || document.body;
			appendTarget.appendChild(this.DOM.details);
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

	DOM.adminItems = document.querySelectorAll('.user-stat-item');
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

// Filter functions
let currentSortColumn = 'Surname';
let currentSortOrder = 'asc';

document.addEventListener('DOMContentLoaded', function() {
    initializeSortingAndFiltering();
});

function initializeSortingAndFiltering() {
    const currentPagePath = window.location.pathname;
    let filterFunction;
    let searchInputId;

    // Determine which page we're on and set the appropriate filter function and search input ID
    if (currentPagePath.includes('/customers/customer_list')) {
        filterFunction = filterCustomers;
        searchInputId = 'listCustomerSearch';
    } else if (currentPagePath.includes('/account_list')) {
        filterFunction = filterAccounts;
        searchInputId = 'listAccountSearch';
    }

    // Proceed with setting up sorting and the search event listener if on a recognized page
    if (filterFunction && searchInputId) {
        // Sorting Event Listeners
        setupSorting(filterFunction);

        // Initial fetch with default sort parameters
        filterFunction();

        // Search Event Listener
        const searchInput = document.getElementById(searchInputId);
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                filterFunction(1, currentSortColumn, currentSortOrder);
            });
        }
    }
}

function setupSorting(filterFunction) {
    document.querySelectorAll('.sortable-column').forEach(column => {
        column.addEventListener('click', () => {
            const sortColumn = column.getAttribute('data-sort-column');
            const newSortOrder = column.getAttribute('data-sort-order') === 'asc' ? 'desc' : 'asc';

            // Update UI for sorting
            updateSortingUI(column, newSortOrder);
            // Fetch with new sort parameters
            filterFunction(1, sortColumn, newSortOrder);
        });
    });
}

function updateSortingUI(column, newSortOrder) {
    // First, remove existing arrows from all sortable columns
    document.querySelectorAll('.sortable-column').forEach(col => {
        col.innerHTML = col.innerHTML.replace(' ↑', '').replace(' ↓', ''); // Adjust based on your actual content
    });

    // Then, append the correct arrow to the clicked column header based on the new sort order
    const arrow = newSortOrder === 'asc' ? ' ↑' : ' ↓';
    column.innerHTML += arrow;
}


function filterCustomers(pageNum = 1) {
    let searchQuery = document.getElementById('listCustomerSearch').value;

    fetch(`/customers/customer_list?ajax=1&search=${encodeURIComponent(searchQuery)}&page=${pageNum}&sort_column=${currentSortColumn}&sort_order=${currentSortOrder}`)
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('customerListBody');
        if (!tbody) {
            console.error('Tbody element not found');
            return;
        }

        tbody.innerHTML = '';

        if (data.customers && data.customers.length) {
            data.customers.forEach(customer => {
                const row = document.createElement('tr');
                row.className = 'table-row';
                row.setAttribute('data-customer', JSON.stringify(customer));
                row.innerHTML = `
                    <td>${customer.Surname}, ${customer.GivenName}</td>
                    <td>${customer.Country}</td>
                    <td>${customer.Telephone}</td>
                    <td>${customer.EmailAddress}</td>
                    <td>${customer.PersonalNumber}</td>
                    <td class="details-link">Details</td>
                `;

                // Attach click event listener for each row
                row.addEventListener('click', () => {
                    DOM.details.fillCustomerData(customer);
                    DOM.details.open();
                });

                tbody.appendChild(row);
            });
			updatePaginationControls(data.pagination);
        } else {
            tbody.innerHTML = '<tr><td colspan="6">No customers found.</td></tr>';
        }
    })
    .catch(error => console.error('Error during fetch:', error));
}

function filterAccounts(pageNum = 1, sortColumn = 'Surname', sortOrder = 'asc') {
    let searchQuery = document.getElementById('listAccountSearch').value;

    fetch(`/account_list?ajax=1&search=${encodeURIComponent(searchQuery)}&page=${pageNum}&sort_column=${sortColumn}&sort_order=${sortOrder}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const tbody = document.querySelector('#accountListBody');
        tbody.innerHTML = '';

        data.customers.forEach(customer => {
            const row = document.createElement('tr');
            row.className = 'table-row';
            let accountsHtml = '<td colspan="2"><table class="inner-table">';

            Object.entries(customer.GroupedAccounts).forEach(([accountType, accountInfo]) => {
                accountsHtml += `<tr><td>${accountType} x ${accountInfo.count}</td><td>${accountInfo.total_balance} SEK</td></tr>`;
            });
            accountsHtml += '</table></td>';

            row.innerHTML = `<td>${customer.Surname}, ${customer.GivenName}</td>${accountsHtml}<td>${customer.total_balance} SEK</td>`;
            
			// Attach click event listener for each row
			row.addEventListener('click', () => {
				DOM.details.fillCustomerData(customer);
				DOM.details.open();
			});
			
			tbody.appendChild(row);
        });

        updatePaginationControls(data.pagination);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// pagination handling

function updatePaginationControls(pagination) {
    const paginationContainer = document.querySelector('.table-row-pagination');
    paginationContainer.innerHTML = ''; // Clear existing controls

    // Previous page link
    if (pagination.has_prev) {
        const prevLink = document.createElement('a');
        prevLink.href = "#";
        prevLink.innerHTML = "&lt;";
        prevLink.addEventListener('click', (e) => {
            e.preventDefault();
            changePage(pagination.prev_num);
        });
        paginationContainer.appendChild(prevLink);
    }
	// calc for page display amount
	const total_pages = pagination.total_pages;
    const current_page = pagination.current_page;
    const rangeStart = Math.max(1, current_page - 1);
    const rangeEnd = Math.min(total_pages, current_page + 1);

	if (rangeStart > 1) {
        appendPageLink(1);
        if (rangeStart > 2) {
            appendDots();
        }
    }

	for (let i = rangeStart; i <= rangeEnd; i++) {
        appendPageLink(i);
    }

	if (rangeEnd < total_pages) {
        if (rangeEnd < total_pages - 1) {
            appendDots();
        }
        appendPageLink(total_pages);
    }

	// next page link
	if (pagination.has_next) {
        const nextLink = document.createElement('a');
        nextLink.href = "#";
        nextLink.innerHTML = "&gt;";
        nextLink.addEventListener('click', (e) => {
            e.preventDefault();
            changePage(pagination.next_num);
        });
        paginationContainer.appendChild(nextLink);
    }

    function appendPageLink(page) {
        const pageLink = document.createElement('a');
        pageLink.href = "#";
        pageLink.innerText = page;
        if (page === current_page) {
            pageLink.classList.add('active');
        } else {
            pageLink.addEventListener('click', (e) => {
                e.preventDefault();
                changePage(page);
            });
        }
        paginationContainer.appendChild(pageLink);
    }

	function appendDots() {
        const dots = document.createElement('span');
		dots.className = "dots"
        dots.innerText = '...';
        paginationContainer.appendChild(dots);
    }
}

function changePage(pageNum) {
    const currentPagePath = window.location.pathname;
    if (currentPagePath.includes('/customers/customer_list')) {
        filterCustomers(pageNum, currentSortColumn, currentSortOrder);
    } else if (currentPagePath.includes('/account_list')) {
        filterAccounts(pageNum, currentSortColumn, currentSortOrder);
    }
}

// filter end

// sidebar collapse
document.addEventListener("DOMContentLoaded", function() {
    const sidebarWrapper = document.getElementById('sidebar-wrapper');
    const sidebarToggle = document.getElementById('sidebarToggle');

    // Function to toggle sidebar state
    function toggleSidebar() {
        const isCollapsed = sidebarWrapper.classList.contains('collapsed');
        sidebarWrapper.classList.toggle('collapsed', !isCollapsed);
        localStorage.setItem('sidebarCollapsed', !isCollapsed);
    }

    // Set initial state of sidebar from localStorage
    const sidebarShouldBeCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (sidebarShouldBeCollapsed) {
        sidebarWrapper.classList.add('collapsed');
    } else {
        sidebarWrapper.classList.remove('collapsed');
    }

    // Toggle sidebar on button click
    sidebarToggle.addEventListener('click', toggleSidebar);
});

//sidebar end

//Graph functionality
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

const navToggle = document.getElementById('navToggle');
if (navToggle) {
    navToggle.addEventListener('click', function() {
        var linksContainer = document.querySelector('.tm-nav-table-container');
        var mainContent = document.querySelector('.tm-main-content');
        if (linksContainer && mainContent) {
            linksContainer.classList.toggle('active');

            if (linksContainer.classList.contains('active')) {
                mainContent.style.marginTop = (linksContainer.offsetHeight + 60) + 'px';
            } else {
                mainContent.style.marginTop = '60px';
            }
        }
    });
}

// Collapse sidebar when window is too small

document.addEventListener('DOMContentLoaded', function() {
    var navigation = document.getElementById('sidebar-wrapper');

    if (window.innerWidth < 768) {
        navigation.classList.add('collapsed');
    }
});

// dropdown search functionality.

function searchInformation() {
    var input = document.getElementById('headerCustomerSearch');
    var filter = input.value.trim();
    var dropdown = document.getElementById('searchDropdown');

    if (!filter) {
        dropdown.style.display = 'none';
        return;
    }

    fetch(`/search_customers?search=${encodeURIComponent(filter)}&ajax=1`)
        .then(response => response.json())
        .then(data => {
            dropdown.innerHTML = ''; // Clear previous results
            
            if (data.length > 0) {
                // Limit name matches to the first 5 results for closest name matches
                const nameMatches = data.slice(0, 5);
                nameMatches.forEach(customer => appendCustomerToDropdown(customer, dropdown));
                
                // Add a divider
                if (data.length > 5) { // Only add a divider if there are more than 5 results
                    let divider = document.createElement('div');
                    divider.className = 'dropdown-divider';
                    divider.textContent = '---'; // Placeholder divider, adjust as needed
                    dropdown.appendChild(divider);

                    // Append other category placeholders after the divider
                    // Placeholder for demonstration, replace with actual data/categories as needed
                    let placeholder = document.createElement('div');
                    placeholder.className = 'dropdown-item';
                    placeholder.textContent = 'Other Categories...';
                    dropdown.appendChild(placeholder);
                }

                dropdown.style.display = 'block';
            } else {
                dropdown.innerHTML = '<div class="dropdown-item">No results found</div>';
                dropdown.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function appendCustomerToDropdown(customer, dropdown) {
    let customerDiv = document.createElement('div');
    customerDiv.textContent = customer.name;
    customerDiv.className = 'dropdown-item';
    customerDiv.addEventListener('click', function() {
        window.location.href = `/customer_detail/${customer.id}`;
    });
    dropdown.appendChild(customerDiv);
}
$('#headerCustomerSearch').on('input', searchInformation);


window.openDetailsWithData = openDetailsWithData;
